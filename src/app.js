(function (){
  const cfg = window.LASTWISH_CONFIG || {};
  const $ = (s)=>document.querySelector(s);
  const $$ = (s)=>Array.from(document.querySelectorAll(s));

  // Header Reset
  const btnResetApp = $("#btnResetApp");

  // Owner Information elements
  const ownerName = $("#ownerName");
  const primaryWallet = $("#primaryWallet");
  const specialInstructions = $("#specialInstructions");

  // Multiple Wallets elements
  const newWalletAddress = $("#newWalletAddress");
  const btnAddWallet = $("#btnAddWallet");
  const tblWallets = $("#tblWallets tbody");

  // Wallet elements
  const btnConnect=$("#btnConnect"),btnSign=$("#btnSign"),btnDisconnect=$("#btnDisconnect"),connStatus=$("#connStatus");
  const acctEl=$("#acct"),acctEns=$("#acctEns"),chainEl=$("#chain"),accountInfo=$("#accountInfo"),sigStatus=$("#sigStatus");
  const btnPay=$("#btnPay"),payStatus=$("#payStatus"),payAmountLabel=$("#payAmountLabel"),payDiscount=$("#payDiscount"),receiptBox=$("#receiptBox"),txhashEl=$("#txhash"),blocknumEl=$("#blocknum");
  const btnPrint=$("#btnPrint"),yearEl=$("#year");

  // Beneficiaries
  const bName=$("#bName"), bAddressOrEns=$("#bAddressOrEns"), bEmail=$("#bEmail"), bRelation=$("#bRelation"), btnAddBeneficiary=$("#btnAddBeneficiary"), tblBeneficiaries=$("#tblBeneficiaries tbody");

  // Assets
  const btnLoadAssets=$("#btnLoadAssets"), btnLoadDemo=$("#btnLoadDemo"), assetsError=$("#assetsError"), assetsWrap=$("#assetsWrap"), tblTokens=$("#tblTokens tbody"), tblNFTs=$("#tblNFTs tbody"), btnSaveMap=$("#btnSaveMap"), saveStatus=$("#saveStatus");

  yearEl.textContent = new Date().getFullYear();
  payAmountLabel.textContent = String(cfg.payAmountEth || 0);

  // State
  let currentAccount=null,currentChainId=null,currentEns=null,sessionSig=null,sessionNonce=null;
  let beneficiaries=[], assignments={}, additionalWallets=[]; // assignments: key => [{beneficiaryId,percent}]
  const basePrice=Number(cfg.payAmountEth||0);

  // Helpers
  const S={ key:(n)=>`${n}_${(currentAccount||'').toLowerCase()}`, load:(k)=>{try{return JSON.parse(localStorage.getItem(k)||'null')}catch{return null}}, save:(k,v)=>localStorage.setItem(k,JSON.stringify(v)) };
  function short(a){return a?a.slice(0,6)+"…"+a.slice(-4):"";}
  function formatEth(n){return (Math.round(Number(n)*1e6)/1e6).toString();}
  function priceWithDiscount(){ return (currentEns && cfg.ensDiscountPercent>0) ? Math.max(basePrice*(1-cfg.ensDiscountPercent/100),0) : basePrice; }
  function setPriceLabels(){ const base=basePrice, fin=priceWithDiscount(); if(fin<base){ payAmountLabel.textContent=formatEth(fin); payDiscount.textContent=`(${formatEth(base)} ETH)`; payDiscount.classList.remove("hidden"); } else { payAmountLabel.textContent=formatEth(base); payDiscount.classList.add("hidden"); } }

  function clearListeners(){ if(window.ethereum && window.ethereum.removeAllListeners){ try{window.ethereum.removeAllListeners("accountsChanged");}catch{} try{window.ethereum.removeAllListeners("chainChanged");}catch{} } }
  function resetApp(){
    clearListeners();
    const keys = Object.keys(localStorage).filter(k=>k.startsWith("lastwish_"));
    keys.forEach(k=>localStorage.removeItem(k));
    currentAccount=null; currentChainId=null; currentEns=null; sessionSig=null; sessionNonce=null;
    additionalWallets=[]; ownerName.value=""; specialInstructions.value=""; primaryWallet.value="";
    acctEl.textContent=""; chainEl.textContent=""; acctEns.classList.add("hidden"); acctEns.textContent="";
    accountInfo.classList.add("hidden"); connStatus.textContent="Not connected";
    btnSign.disabled=true; btnDisconnect.disabled=true; btnLoadAssets.disabled=true; btnPay.disabled=true; btnPrint.disabled=true;
    assetsWrap.classList.add("hidden"); assetsError.textContent=""; tblTokens.innerHTML=""; tblNFTs.innerHTML="";
    refreshWalletsTable();
    if (cfg.n8nWebhookUrl){ fetch(cfg.n8nWebhookUrl,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event:"app_reset",timestamp:new Date().toISOString()})}).catch(()=>{}); }
  }

  // Storage
  function loadAll(){ 
    beneficiaries = S.load(S.key("lastwish_beneficiaries_v3")) || []; 
    assignments = S.load(S.key("lastwish_assignments_v3")) || {}; 
    additionalWallets = S.load(S.key("lastwish_wallets_v3")) || [];
    const savedOwnerName = S.load(S.key("lastwish_owner_name_v3"));
    const savedInstructions = S.load(S.key("lastwish_special_instructions_v3"));
    if(savedOwnerName) ownerName.value = savedOwnerName;
    if(savedInstructions) specialInstructions.value = savedInstructions;
  }
  function saveAll(){ 
    S.save(S.key("lastwish_beneficiaries_v3"), beneficiaries); 
    S.save(S.key("lastwish_assignments_v3"), assignments); 
    S.save(S.key("lastwish_wallets_v3"), additionalWallets);
    S.save(S.key("lastwish_owner_name_v3"), ownerName.value);
    S.save(S.key("lastwish_special_instructions_v3"), specialInstructions.value);
  }

  // Multiple Wallets Management
  function refreshWalletsTable() {
    tblWallets.innerHTML = "";
    additionalWallets.forEach((wallet, index) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${short(wallet.address)}</td>
        <td>${wallet.ens || ""}</td>
        <td class="right"><button onclick="removeWallet(${index})" class="btn btn-danger btn-sm">Remove</button></td>
      `;
      tblWallets.appendChild(tr);
    });
  }

  async function addWallet() {
    const address = newWalletAddress.value.trim();
    if (!address) {
      alert("Please enter a wallet address or ENS name");
      return;
    }

    if (additionalWallets.length >= 20) {
      alert("Maximum of 20 wallets allowed");
      return;
    }

    // Check if wallet already exists
    if (additionalWallets.some(w => w.address.toLowerCase() === address.toLowerCase())) {
      alert("This wallet address is already added");
      return;
    }

    try {
      let resolvedAddress = address;
      let ensName = "";

      // Try to resolve ENS if it ends with .eth
      if (address.endsWith('.eth')) {
        try {
          const response = await fetch(`https://deep-index.moralis.io/api/v2.2/resolve/ens/${address}`, {
            headers: { 'X-API-Key': cfg.moralisApiKey }
          });
          if (response.ok) {
            const data = await response.json();
            if (data.address) {
              resolvedAddress = data.address;
              ensName = address;
            }
          }
        } catch (e) {
          console.warn('ENS resolution failed:', e);
        }
      }

      additionalWallets.push({
        address: resolvedAddress,
        ens: ensName,
        id: Date.now()
      });

      newWalletAddress.value = "";
      refreshWalletsTable();
      saveAll();
    } catch (error) {
      console.error('Error adding wallet:', error);
      alert("Error adding wallet. Please check the address and try again.");
    }
  }

  function removeWallet(index) {
    additionalWallets.splice(index, 1);
    refreshWalletsTable();
    saveAll();
  }

  // Make removeWallet globally accessible
  window.removeWallet = removeWallet;

  // Wallet connect/sign/disconnect
  async function ensureChain(id){ try{ await window.ethereum.request({method:"wallet_switchEthereumChain",params:[{chainId:"0x"+Number(id).toString(16)}]}); return true;}catch{ return false;} }
  async function connect(){
    if(!window.ethereum){ alert("Install MetaMask/Coinbase Wallet."); return; }
    connStatus.textContent="Connecting…";
    try{
      await window.ethereum.request({method:"eth_requestAccounts"});
      const accounts=await window.ethereum.request({method:"eth_accounts"});
      const cidHex=await window.ethereum.request({method:"eth_chainId"});
      const cid=parseInt(cidHex,16);
      if (cfg.chainId && cid!==cfg.chainId) await ensureChain(cfg.chainId);
      currentAccount=accounts[0]; currentChainId=cfg.chainId||cid;
      acctEl.textContent=currentAccount; chainEl.textContent=currentChainId; accountInfo.classList.remove("hidden");
      connStatus.textContent=`Connected as ${short(currentAccount)}`;
      btnSign.disabled=false; btnDisconnect.disabled=false; btnLoadAssets.disabled=false; btnPay.disabled=false;

      // Update primary wallet field
      primaryWallet.value = currentAccount;

      // reverse ENS
      try{ const r=await fetch(`/.netlify/functions/moralis-proxy?route=reverseEns&address=${currentAccount}`); const d=await r.json(); if(d && d.name){ currentEns=d.name; acctEns.textContent=currentEns; acctEns.classList.remove("hidden"); } }catch{}
      setPriceLabels();

      window.ethereum.on("accountsChanged",(accs)=>{ if(accs&&accs.length){ currentAccount=accs[0]; acctEl.textContent=currentAccount; connStatus.textContent=`Connected as ${short(currentAccount)}`; primaryWallet.value=currentAccount; sessionSig=null; sessionNonce=null; acctEns.classList.add("hidden"); setPriceLabels(); } });
      window.ethereum.on("chainChanged",(c)=>{ currentChainId=parseInt(c,16); chainEl.textContent=currentChainId; setPriceLabels(); });
      loadAll(); renderBeneficiaries(); refreshWalletsTable(); // show existing lists
    }catch(e){ console.error(e); connStatus.textContent="Not connected"; }
  }
  function genNonce(){ return Math.random().toString(36).slice(2)+Date.now().toString(36); }
  async function signSession(){
    if(!currentAccount){ alert("Connect first."); return; }
    sessionNonce=genNonce();
    const msg=`LastWish.eth session\nAddress: ${currentAccount}\nNonce: ${sessionNonce}\nDate: ${new Date().toISOString()}`;
    try{ const sig=await window.ethereum.request({method:"personal_sign",params:[msg,currentAccount]}); sessionSig=sig; localStorage.setItem("lastwish_session_sig",sig); localStorage.setItem("lastwish_session_nonce",sessionNonce); sigStatus.innerHTML='<span class="ok">Signed ✓</span>'; if(cfg.n8nWebhookUrl){ fetch(cfg.n8nWebhookUrl,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event:"session_signed",address:currentAccount,ens:currentEns,nonce:sessionNonce,signature:sig,timestamp:new Date().toISOString()})}).catch(()=>{}); } }catch(e){ sigStatus.innerHTML='<span class="danger">Signature declined</span>'; }
  }
  function disconnect(){ resetApp(); }

  // Beneficiaries
  function renderBeneficiaries(){
    tblBeneficiaries.innerHTML="";
    beneficiaries.forEach((b,i)=>{
      const tr=document.createElement("tr");
      tr.innerHTML=`<td>${b.name||""}</td><td>${b.address||"<span class='muted'>(not set)</span>"}</td><td>${b.ens||""}</td><td>${b.email||""}</td><td>${b.relation||""}</td><td class="right"><button data-i="${i}" class="btn" style="background:#fee2e2;color:#991b1b">Delete</button></td>`;
      tblBeneficiaries.appendChild(tr);
    });
    tblBeneficiaries.querySelectorAll("button[data-i]").forEach(btn=>btn.onclick=()=>{ const idx=Number(btn.dataset.i); const removed=beneficiaries.splice(idx,1)[0]; Object.keys(assignments).forEach(k=>{ assignments[k]=(assignments[k]||[]).filter(a=>a.beneficiaryId!==removed.id); if(!assignments[k].length) delete assignments[k];}); saveAll(); renderBeneficiaries(); refreshAssignmentUIs(); });
  }
  async function addBeneficiary(){
    const name=bName.value.trim(), addrOrEns=bAddressOrEns.value.trim(), email=bEmail.value.trim(), relation=bRelation.value.trim();
    if(!name){ alert("Name is required."); return; }
    let address="", ens="";
    if (addrOrEns){
      if (/\.eth$/i.test(addrOrEns)){
        try{ 
          // Direct ENS resolution via Moralis API
          const response = await fetch(`https://deep-index.moralis.io/api/v2.2/resolve/ens/${encodeURIComponent(addrOrEns)}`, {
            headers: {
              'Accept': 'application/json',
              'X-API-Key': cfg.moralisApiKey
            }
          });
          if (response.ok) {
            const data = await response.json();
            if (data && data.address) { 
              address = data.address; 
              ens = addrOrEns; 
            } else { 
              alert("ENS not found. Saving without address."); 
            }
          } else {
            alert("ENS lookup failed. Saving without address.");
          }
        } catch { 
          alert("ENS lookup failed. Saving without address."); 
        }
      } else if (/^0x[a-fA-F0-9]{40}$/.test(addrOrEns)){ 
        address=addrOrEns; 
      } else { 
        alert("Enter a valid 0x address, an ENS (alice.eth), or leave blank."); 
        return; 
      }
    }
    const id="b_"+Date.now()+"_"+Math.random().toString(36).slice(2,7);
    beneficiaries.push({id,name,address,ens,email,relation});
    
    // Auto-calculate percentages for all existing assignments
    redistributePercentages();
    
    bName.value=""; bAddressOrEns.value=""; bEmail.value=""; bRelation.value="";
    saveAll(); renderBeneficiaries(); refreshAssignmentUIs();
  }

  // Auto-percentage redistribution function
  function redistributePercentages() {
    const numBeneficiaries = beneficiaries.length;
    if (numBeneficiaries === 0) return;
    
    const percentPerBeneficiary = Math.floor(100 / numBeneficiaries);
    const remainder = 100 - (percentPerBeneficiary * numBeneficiaries);
    
    // Update all existing assignments
    Object.keys(assignments).forEach(key => {
      if (assignments[key] && assignments[key].length > 0) {
        // Clear existing assignments and redistribute
        assignments[key] = beneficiaries.map((b, index) => ({
          beneficiaryId: b.id,
          percent: index === 0 ? percentPerBeneficiary + remainder : percentPerBeneficiary
        }));
      }
    });
  }

  // Assets & assignments
  function keyERC20(sym,addr){ return `erc20:${sym}:${addr.toLowerCase()}`; }
  function keyNFT(col,id){ return `nft:${col.toLowerCase()}:${id}`; }
  function beneOptions(){ return beneficiaries.map(b=>`<option value="${b.id}">${b.name} ${b.ens?`(${b.ens})`:(b.address?`(${short(b.address)})`:"")}</option>`).join(""); }
  function rowsHtml(key){
    const rows=(assignments[key]||[]);
    const opts=beneOptions();
    const body=rows.map((a,i)=>`<div class="row mt4" data-row="${i}"><select class="assignee">${opts}</select><input class="percent" type="text" placeholder="%" value="${a.percent||""}" style="width:80px;margin-left:8px"><button class="btn" style="background:#fee2e2;color:#991b1b;margin-left:8px" data-action="remove">Remove</button></div>`).join("");
    return `<div class="assignments" data-key="${key}">${body || "<div class='muted'>No assignments yet.</div>"}<div class="mt8"><button class="btn" data-action="add" style="background:#e2e8f0;color:#0f172a">Add Split</button></div></div>`;
  }
  function wireAssign(container){
    container.querySelectorAll(".assignments").forEach(block=>{
      const key=block.dataset.key;
      (assignments[key]||[]).forEach((a,i)=>{
        const selects=block.querySelectorAll("select.assignee");
        if(selects[i]) selects[i].value=a.beneficiaryId;
      });
      block.addEventListener("click",(e)=>{
        const t=e.target;
        if(t.matches("button[data-action='add']")){
          assignments[key]=assignments[key]||[];
          const first=beneficiaries[0];
          assignments[key].push({beneficiaryId:first?first.id:"",percent:""});
          
          // Auto-calculate percentages for this asset
          autoCalculatePercentagesForAsset(key);
          
          block.outerHTML=rowsHtml(key); wireAssign(document);
        } else if(t.matches("button[data-action='remove']")){
          const row=t.closest("[data-row]"); const idx=Number(row.dataset.row);
          assignments[key].splice(idx,1);
          
          // Auto-calculate percentages for remaining assignments
          if(assignments[key].length > 0) {
            autoCalculatePercentagesForAsset(key);
          }
          
          block.outerHTML=rowsHtml(key); wireAssign(document);
        }
      });
      block.addEventListener("change",(e)=>{
        if(e.target.matches("select.assignee") || e.target.matches("input.percent")){
          const rows=Array.from(block.querySelectorAll("[data-row]"));
          assignments[key]=rows.map(r=>{
            return { beneficiaryId: r.querySelector("select.assignee").value, percent: r.querySelector("input.percent").value };
          });
        }
      });
    });
  }

  // Auto-calculate percentages for a specific asset
  function autoCalculatePercentagesForAsset(key) {
    if (!assignments[key] || assignments[key].length === 0) return;
    
    const numAssignments = assignments[key].length;
    const percentPerAssignment = Math.floor(100 / numAssignments);
    const remainder = 100 - (percentPerAssignment * numAssignments);
    
    assignments[key].forEach((assignment, index) => {
      assignment.percent = index === 0 ? percentPerAssignment + remainder : percentPerAssignment;
    });
  }
  function refreshAssignmentUIs(){ $$(".assignments").forEach(b=>{ const key=b.dataset.key; b.outerHTML=rowsHtml(key); }); wireAssign(document); }

  async function callProxy(url){
    assetsError.textContent=""; const r=await fetch(url,{headers:{"Accept":"application/json"}}); const tx=await r.text(); if(!r.ok){ assetsError.textContent=`Proxy error ${r.status}: ${tx}`; throw new Error(tx); } try{return JSON.parse(tx);}catch{return{};}
  }

  async function loadAssets(){
    if(!currentAccount){ alert("Connect first."); return; }
    assetsWrap.classList.add("hidden"); tblTokens.innerHTML=""; tblNFTs.innerHTML="";
    assetsError.textContent="Loading assets...";
    
    try{
      // Direct Moralis API call for ERC-20 tokens
      const tokenResponse = await fetch(`https://deep-index.moralis.io/api/v2.2/${currentAccount}/erc20?chain=eth`, {
        headers: {
          'Accept': 'application/json',
          'X-API-Key': cfg.moralisApiKey
        }
      });
      
      if (!tokenResponse.ok) {
        throw new Error(`Token API error: ${tokenResponse.status}`);
      }
      
      const tokenData = await tokenResponse.json();
      (tokenData.result || tokenData || []).forEach(x=>{
        const tr=document.createElement("tr");
        const sym=x.symbol||"TOK"; const dec=Number(x.decimals||18);
        let human="0"; try{ human=(Number(BigInt(x.balance||"0"))/(10**dec)).toString(); }catch{}
        const key=keyERC20(sym,x.token_address);
        tr.innerHTML=`<td><span class="pill">${sym}</span> <span class="small">${x.token_address.slice(0,6)}…${x.token_address.slice(-4)}</span></td><td>${human}</td><td>${rowsHtml(key)}</td>`;
        tblTokens.appendChild(tr);
      });
      
      // Direct Moralis API call for NFTs
      const nftResponse = await fetch(`https://deep-index.moralis.io/api/v2.2/${currentAccount}/nft?chain=eth&format=decimal&limit=10`, {
        headers: {
          'Accept': 'application/json',
          'X-API-Key': cfg.moralisApiKey
        }
      });
      
      if (!nftResponse.ok) {
        throw new Error(`NFT API error: ${nftResponse.status}`);
      }
      
      const nftData = await nftResponse.json();
      (nftData.result || nftData || []).forEach(x=>{
        const tr=document.createElement("tr");
        const col=x.token_address, id=x.token_id;
        const key=keyNFT(col,id);
        const name = x.name || x.metadata?.name || "NFT";
        tr.innerHTML=`<td><span class="pill">${name}</span> <span class="small">${col.slice(0,6)}…${col.slice(-4)}</span></td><td>#${id}</td><td>${rowsHtml(key)}</td>`;
        tblNFTs.appendChild(tr);
      });
      
      assetsError.textContent="";
      assetsWrap.classList.remove("hidden"); 
      refreshAssignmentUIs();
      
    } catch(e) {
      console.error('Asset loading error:', e);
      assetsError.textContent = `Error loading assets: ${e.message}. Please try the demo data instead.`;
    }
  }

  function loadDemoAssets(){
    assetsWrap.classList.add("hidden"); tblTokens.innerHTML=""; tblNFTs.innerHTML="";
    assetsError.textContent="";
    
    // Demo ERC-20 tokens
    const demoTokens = [
      {symbol: "USDC", token_address: "0xA0b86a33E6441e8e421f8e2b4b8b6b8b8b8b8b8b", balance: "1000000000", decimals: 6},
      {symbol: "WETH", token_address: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", balance: "2500000000000000000", decimals: 18},
      {symbol: "UNI", token_address: "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", balance: "50000000000000000000", decimals: 18}
    ];
    
    demoTokens.forEach(x=>{
      const tr=document.createElement("tr");
      const sym=x.symbol||"TOK"; const dec=Number(x.decimals||18);
      let human="0"; try{ human=(Number(BigInt(x.balance||"0"))/(10**dec)).toString(); }catch{}
      const key=keyERC20(sym,x.token_address);
      tr.innerHTML=`<td><span class="pill">${sym}</span> <span class="small">${x.token_address.slice(0,6)}…${x.token_address.slice(-4)}</span></td><td>${human}</td><td>${rowsHtml(key)}</td>`;
      tblTokens.appendChild(tr);
    });
    
    // Demo NFTs
    const demoNFTs = [
      {name: "Bored Ape", token_address: "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", token_id: "1234"},
      {name: "CryptoPunk", token_address: "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB", token_id: "5678"},
      {name: "Azuki", token_address: "0xED5AF388653567Af2F388E6224dC7C4b3241C544", token_id: "9012"}
    ];
    
    demoNFTs.forEach(x=>{
      const tr=document.createElement("tr");
      const col=x.token_address, id=x.token_id;
      const key=keyNFT(col,id);
      tr.innerHTML=`<td><span class="pill">${x.name||"NFT"}</span> <span class="small">${col.slice(0,6)}…${col.slice(-4)}</span></td><td>#${id}</td><td>${rowsHtml(key)}</td>`;
      tblNFTs.appendChild(tr);
    });
    
    assetsWrap.classList.remove("hidden"); refreshAssignmentUIs();
  }

  function validatePercents(){ for(const [k,rows] of Object.entries(assignments)){ if(!rows||!rows.length) continue; const total=rows.reduce((a,r)=>a+(parseFloat(r.percent||"0")||0),0); if(Math.abs(total-100)>0.001) return {ok:false,key:k,total}; } return {ok:true}; }
  function saveAssignmentClick(){ const v=validatePercents(); if(!v.ok){ alert(`Percentages for ${v.key} must total 100%. Current total: ${v.total}`); return; } saveAll(); saveStatus.textContent="Saved ✅"; setTimeout(()=>saveStatus.textContent="",2000); if(cfg.n8nWebhookUrl){ fetch(cfg.n8nWebhookUrl,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event:"assignments_saved_v3",owner:currentAccount,ens:currentEns,beneficiaries,assignments,timestamp:new Date().toISOString()})}).catch(()=>{}); } }

  // Payment (mainnet)
  async function waitForConfirmation(txHash,pollMs=2000,maxMs=180000){ const start=Date.now(); while(Date.now()-start<maxMs){ try{ const r=await window.ethereum.request({method:"eth_getTransactionReceipt",params:[txHash]}); if(r&&r.blockNumber&&r.status==="0x1") return r; }catch{} await new Promise(r=>setTimeout(r,pollMs)); } throw new Error("Timeout waiting for confirmation"); }
  async function pay(){
    if(!currentAccount){ alert("Connect first."); return; }
    try{
      btnPay.disabled = true; payStatus.textContent = "Sending transaction…";
      const eth = (currentEns && cfg.ensDiscountPercent>0) ? Math.max(Number(cfg.payAmountEth||0)*(1-cfg.ensDiscountPercent/100),0) : Number(cfg.payAmountEth||0);
      const weiHex = "0x" + (BigInt(Math.floor(eth*1e18))).toString(16);
      const txHash = await window.ethereum.request({ method:"eth_sendTransaction", params:[{ from: currentAccount, to: cfg.payToAddress, value: weiHex }] });
      payStatus.textContent="Waiting for confirmation…"; txhashEl.textContent=txHash; txhashEl.href="https://etherscan.io/tx/"+txHash; receiptBox.classList.remove("hidden");
      const receipt=await waitForConfirmation(txHash);
      if (receipt && receipt.status==="0x1"){
        blocknumEl.textContent=parseInt(receipt.blockNumber,16); payStatus.textContent="Payment confirmed ✅"; btnPrint.disabled=false;
        if(cfg.n8nWebhookUrl){ fetch(cfg.n8nWebhookUrl,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event:"payment_confirmed",address:currentAccount,ens:currentEns,hash:txHash,blockNumber:parseInt(receipt.blockNumber,16),chainId:currentChainId,amountEth:String(eth),timestamp:new Date().toISOString()})}).catch(()=>{}); }
      } else { payStatus.textContent="Payment failed ❌"; btnPay.disabled=false; }
    }catch(err){ console.error(err); payStatus.textContent="Payment failed ❌"; btnPay.disabled=false; alert("Payment failed or rejected."); }
  }

  // Print (comprehensive legal document)
  function generatePrintableHtml(){
    const today = new Date().toLocaleDateString();
    const ownerFullName = ownerName.value.trim() || "Digital Asset Owner";
    const primaryWalletAddr = primaryWallet.value || currentAccount || "Primary Wallet Address";
    const instructions = specialInstructions.value.trim();
    
    // Get all wallet addresses (primary + additional)
    const allWallets = [primaryWalletAddr, ...additionalWallets.map(w => w.address)];
    const walletsList = allWallets.map(addr => `<div class="address-box">${addr}</div>`).join("");
    
    // Calculate total portfolio value
    let totalValue = 0;
    const assetLines = [];
    
    for(const [key, rows] of Object.entries(assignments)) {
      if(!rows || !rows.length) continue;
      
      if(key.startsWith("erc20:")) {
        const [, sym, addr] = key.split(":");
        rows.forEach(r => {
          const b = beneficiaries.find(x => x.id === r.beneficiaryId);
          if(b) {
            assetLines.push(`• ${sym} Token (${addr.slice(0,6)}...${addr.slice(-4)}) - ${r.percent}% to ${b.name}${b.ens ? ` (${b.ens})` : ""}`);
          }
        });
      } else if(key.startsWith("nft:")) {
        const [, col, id] = key.split(":");
        rows.forEach(r => {
          const b = beneficiaries.find(x => x.id === r.beneficiaryId);
          if(b) {
            assetLines.push(`• NFT Collection ${col.slice(0,6)}...${col.slice(-4)} Token #${id} - ${r.percent}% to ${b.name}${b.ens ? ` (${b.ens})` : ""}`);
          }
        });
      }
    }
    
    // Get primary executor (first beneficiary)
    const primaryExecutor = beneficiaries.length > 0 ? beneficiaries[0] : null;
    const backupExecutor = beneficiaries.length > 1 ? beneficiaries[1] : null;
    
    // Asset distribution section
    const assetDistribution = beneficiaries.map((b, index) => {
      const percentage = beneficiaries.length === 1 ? 100 : Math.floor(100 / beneficiaries.length);
      const remainder = beneficiaries.length === 1 ? 0 : (100 - (Math.floor(100 / beneficiaries.length) * beneficiaries.length));
      const finalPercentage = index === 0 ? percentage + remainder : percentage;
      
      return `
        <p><strong>${index + 1}. To ${b.name}${b.ens ? ` (${b.ens})` : ""}, with digital wallet address:</strong></p>
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0; background: #f9f9f9; font-family: monospace;">
          ${b.address || b.ens || "(Address to be provided)"}
        </div>
        <p>I hereby bequeath <strong>${finalPercentage}% (${finalPercentage} percent)</strong> of all digital assets described herein, including any future appreciation, forks, airdrops, or derivative assets.</p>
      `;
    }).join("");
    
    return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Last Will and Testament — ${ownerFullName}</title>
  <style>
    body { 
      font-family: 'Times New Roman', Times, serif; 
      line-height: 1.6; 
      margin: 40px; 
      color: #000; 
      max-width: 8.5in;
    }
    h1 { 
      text-align: center; 
      font-size: 24px; 
      margin-bottom: 30px; 
      text-decoration: underline;
    }
    h2 { 
      font-size: 18px; 
      margin-top: 30px; 
      margin-bottom: 15px; 
      text-decoration: underline;
    }
    p { margin: 12px 0; }
    .article { margin: 25px 0; }
    .signature-section { 
      margin-top: 50px; 
      page-break-inside: avoid;
    }
    .signature-line { 
      border-bottom: 1px solid #000; 
      width: 300px; 
      margin: 30px 0 10px 0; 
    }
    .witness-section {
      margin-top: 40px;
      border: 2px solid #000;
      padding: 20px;
    }
    .date-line {
      border-bottom: 1px solid #000;
      width: 200px;
      display: inline-block;
      margin: 0 10px;
    }
    .address-box {
      border: 1px solid #000;
      padding: 10px;
      margin: 10px 0;
      background: #f9f9f9;
      font-family: monospace;
      word-break: break-all;
    }
    .asset-list {
      margin: 15px 0;
      padding-left: 20px;
    }
    .notary-section {
      margin-top: 40px;
      border: 2px solid #000;
      padding: 20px;
      text-align: center;
    }
    .notary-seal {
      border: 2px solid #000;
      width: 150px;
      height: 100px;
      margin: 20px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
    }
    .special-instructions {
      border: 1px solid #000;
      padding: 15px;
      margin: 20px 0;
      background: #f5f5f5;
      font-style: italic;
    }
  </style>
</head>
<body>
  <h1>Last Will and Testament of ${ownerFullName}</h1>
  
  <div class="article">
    <h2>ARTICLE I - DECLARATION AND REVOCATION</h2>
    <p>I, <strong>${ownerFullName}</strong>, a resident of the jurisdiction where this will is executed, being of sound mind and memory and not acting under duress, menace, fraud, or undue influence of any person whomsoever, do hereby make, publish, and declare this instrument to be my Last Will and Testament, hereby expressly revoking all wills and codicils heretofore made by me.</p>
    
    <p>I am over the age of eighteen (18) years and am competent to make this Will. I declare that this Will expresses my true wishes concerning the disposition of my digital assets and that I have carefully read this Will and understand its contents.</p>
  </div>

  <div class="article">
    <h2>ARTICLE II - DIGITAL ASSET IDENTIFICATION AND DISPOSITION</h2>
    <p>I hereby give, devise, and bequeath all of my right, title, and interest in and to my digital assets, including but not limited to cryptocurrency, digital tokens, non-fungible tokens (NFTs), smart contracts, and other blockchain-based assets, currently held in or accessible through the following digital wallet addresses:</p>
    
    ${walletsList}
    
    <p><strong>Current Digital Asset Inventory (as of ${today}):</strong></p>
    <div class="asset-list">
      ${assetLines.length > 0 ? assetLines.map(line => `<p>${line}</p>`).join("") : "<p>• Digital assets to be inventoried at time of distribution</p>"}
    </div>
    
    <p><strong>Total Estimated Portfolio Value:</strong> To be determined at time of distribution</p>
    
    <h3>Asset Distribution:</h3>
    ${assetDistribution}
  </div>

  <div class="article">
    <h2>ARTICLE III - APPOINTMENT OF EXECUTOR AND DIGITAL ASSET POWERS</h2>
    <p>I hereby nominate, constitute, and appoint <strong>${primaryExecutor ? primaryExecutor.name : "To be designated"}</strong> as the Executor of this Last Will and Testament. If ${primaryExecutor ? primaryExecutor.name : "the primary executor"} is unable, unwilling, or fails to qualify as Executor, I nominate and appoint <strong>${backupExecutor ? backupExecutor.name : "To be designated"}</strong> as successor Executor.</p>
    
    <p><strong>Digital Asset Authority:</strong> I specifically grant my Executor the following powers and authorities with respect to my digital assets:</p>
    
    <p>a) To locate, access, and take control of all digital wallets, private keys, seed phrases, passwords, and authentication methods necessary to access my digital assets;</p>
    
    <p>b) To engage qualified blockchain technology experts, cryptocurrency services, or digital asset custodians as necessary;</p>
    
    <p>c) To convert digital assets to fiat currency if required for estate settlement or tax obligations;</p>
    
    <p>d) To create new digital wallets and transfer assets to beneficiaries' designated addresses;</p>
    
    <p>e) To claim any forks, airdrops, staking rewards, or other derivative benefits;</p>
    
    <p>f) To pay all taxes, fees, and expenses related to digital asset management and transfer;</p>
    
    <p>g) To execute all necessary documents and transactions to effectuate the distribution of digital assets.</p>
  </div>

  <div class="article">
    <h2>ARTICLE IV - DIGITAL ASSET ADMINISTRATION INSTRUCTIONS</h2>
    <p><strong>Immediate Actions Required:</strong></p>
    
    <p><strong>1. Security:</strong> My Executor shall immediately secure all digital assets by obtaining control of private keys and changing passwords to prevent unauthorized access;</p>
    
    <p><strong>2. Inventory:</strong> Conduct a complete inventory and valuation of all digital assets within thirty (30) days of my death;</p>
    
    <p><strong>3. Documentation:</strong> Maintain detailed records of all digital asset transactions, including blockchain transaction IDs;</p>
    
    <p><strong>4. Distribution:</strong> Transfer assets to beneficiaries within ninety (90) days unless additional time is required for tax or legal compliance;</p>
    
    <p><strong>5. Tax Compliance:</strong> Ensure all federal, state, and local tax obligations are satisfied before final distribution.</p>
    
    <p><strong>SPECIAL INSTRUCTIONS AND ADDITIONAL WISHES:</strong></p>
    ${instructions ? `<div class="special-instructions">${instructions}</div>` : `<div class="special-instructions"><em>"[No special instructions provided]"</em></div>`}
    
    <p>I direct my Executor to carefully consider and implement these additional instructions to the extent legally permissible and practically feasible. These instructions are an integral part of my wishes for the administration of my digital assets.</p>
  </div>

  <div class="article">
    <h2>ARTICLE V - GENERAL PROVISIONS AND GOVERNING LAW</h2>
    <p><strong>Governing Law:</strong> This Will shall be construed and administered according to the laws of the state of my domicile at the time of my death, without regard to conflict of laws principles.</p>
    
    <p><strong>Severability:</strong> If any provision of this Will is held to be invalid or unenforceable, such determination shall not affect the validity or enforceability of the remaining provisions, which shall continue in full force and effect.</p>
    
    <p><strong>Digital Asset Definition:</strong> "Digital assets" as used herein includes cryptocurrency, virtual currency, digital tokens, non-fungible tokens (NFTs), blockchain-based assets, smart contracts, and any other form of digital property that exists on a blockchain or distributed ledger.</p>
  </div>

  <div class="signature-section">
    <p><strong>IN WITNESS WHEREOF,</strong> I have signed my name to this Last Will and Testament this <span class="date-line"></span> day of <span class="date-line"></span>, 20<span class="date-line"></span>.</p>
    
    <p style="margin-top: 40px;"><strong>TESTATOR:</strong></p>
    <div class="signature-line"></div>
    <p style="text-align: center; margin-top: 10px;"><strong>${ownerFullName}</strong><br>(Signature)</p>
  </div>

  <div class="witness-section">
    <h3 style="text-align: center; margin-top: 0;">ATTESTATION OF WITNESSES</h3>
    
    <p>Each of us declares under penalty of perjury that the following is true and correct:</p>
    
    <p>a) The testator signed this Will in our presence;</p>
    <p>b) The testator appeared to be of sound mind and under no duress;</p>
    <p>c) We signed as witnesses in the testator's presence and in each other's presence;</p>
    <p>d) Each of us is over 18 years of age;</p>
    <p>e) Neither of us is a beneficiary of this Will.</p>
    
    <div style="display: flex; justify-content: space-between; margin-top: 30px;">
      <div style="width: 45%;">
        <p><strong>WITNESS 1:</strong></p>
        <div class="signature-line"></div>
        <p><strong>Print Name:</strong> <span class="date-line"></span></p>
        <p><strong>Address:</strong></p>
        <div class="date-line" style="width: 100%; margin: 5px 0;"></div>
        <div class="date-line" style="width: 100%; margin: 5px 0;"></div>
        <p><strong>Date:</strong> <span class="date-line"></span></p>
      </div>
      
      <div style="width: 45%;">
        <p><strong>WITNESS 2:</strong></p>
        <div class="signature-line"></div>
        <p><strong>Print Name:</strong> <span class="date-line"></span></p>
        <p><strong>Address:</strong></p>
        <div class="date-line" style="width: 100%; margin: 5px 0;"></div>
        <div class="date-line" style="width: 100%; margin: 5px 0;"></div>
        <p><strong>Date:</strong> <span class="date-line"></span></p>
      </div>
    </div>
  </div>

  <div class="notary-section">
    <h3>NOTARIAL ACKNOWLEDGMENT</h3>
    
    <p><strong>State of:</strong> <span class="date-line"></span></p>
    <p><strong>County of:</strong> <span class="date-line"></span></p>
    
    <p>On this <span class="date-line"></span> day of <span class="date-line"></span>, 20<span class="date-line"></span>, before me personally appeared <strong>${owner}</strong>, who proved to me on the basis of satisfactory evidence to be the person whose name is subscribed to the within instrument and acknowledged to me that he/she executed the same in his/her authorized capacity.</p>
    
    <p>I certify under <strong>PENALTY OF PERJURY</strong> under the laws of the State of <span class="date-line"></span> that the foregoing paragraph is true and correct.</p>
    
    <div style="margin-top: 40px;">
      <div class="signature-line" style="margin: 0 auto;"></div>
      <p style="text-align: center;">(Signature of Notary Public)</p>
      
      <div class="notary-seal">
        <div>
          <strong>NOTARY SEAL</strong><br>
          <small>(Affix Official Seal Above)</small>
        </div>
      </div>
      
      <p><strong>My commission expires:</strong> <span class="date-line"></span></p>
    </div>
  </div>

</body>
</html>`;
  }
  function handlePrint(){ const html=generatePrintableHtml(); const w=window.open("", "_blank"); w.document.open(); w.document.write(html); w.document.close(); }

  // Wire
  btnResetApp.addEventListener("click", resetApp);
  $("#btnConnect").addEventListener("click", connect);
  $("#btnSign").addEventListener("click", signSession);
  $("#btnDisconnect").addEventListener("click", disconnect);
  $("#btnAddBeneficiary").addEventListener("click", addBeneficiary);
  $("#btnLoadAssets").addEventListener("click", loadAssets);
  $("#btnLoadDemo").addEventListener("click", loadDemoAssets);
  $("#btnSaveMap").addEventListener("click", saveAssignmentClick);
  $("#btnPay").addEventListener("click", pay);
  $("#btnPrint").addEventListener("click", handlePrint);
  $("#btnAddWallet").addEventListener("click", addWallet);
  
  // Auto-save owner name and special instructions
  $("#ownerName").addEventListener("input", saveAll);
  $("#specialInstructions").addEventListener("input", saveAll);
})();

// Global handlePrint function (outside IIFE) - Mobile Compatible
function handlePrint() {
  const ownerFullName = document.querySelector("#ownerName").value || "To be filled";
  const specialInstructionsText = document.querySelector("#specialInstructions").value || "";
  const primaryWalletAddress = window.currentAccount || "To be connected";
  
  // Get additional wallets
  const additionalWallets = Array.from(document.querySelectorAll("#tblWallets tbody tr")).map(row => {
    const cells = row.querySelectorAll("td");
    return {
      address: cells[0]?.textContent || "",
      ens: cells[1]?.textContent || ""
    };
  });
  
  // Get beneficiaries
  const beneficiaries = Array.from(document.querySelectorAll("#tblBeneficiaries tbody tr")).map(row => {
    const cells = row.querySelectorAll("td");
    return {
      name: cells[0]?.textContent || "",
      address: cells[1]?.textContent || "",
      ens: cells[2]?.textContent || "",
      email: cells[3]?.textContent || "",
      relationship: cells[4]?.textContent || ""
    };
  });
  
  const primaryExecutor = beneficiaries.find(b => b.relationship.toLowerCase().includes("executor")) || beneficiaries[0];
  const backupExecutor = beneficiaries.find(b => b !== primaryExecutor && b.relationship.toLowerCase().includes("executor")) || beneficiaries[1];
  
  // Get assets
  const tokenRows = Array.from(document.querySelectorAll("#tblTokens tbody tr"));
  const nftRows = Array.from(document.querySelectorAll("#tblNFTs tbody tr"));
  
  const assetLines = [];
  tokenRows.forEach(row => {
    const cells = row.querySelectorAll("td");
    const symbol = cells[0]?.textContent || "";
    const balance = cells[1]?.textContent || "";
    if (symbol && balance) {
      assetLines.push(`• ${balance} ${symbol}`);
    }
  });
  
  nftRows.forEach(row => {
    const cells = row.querySelectorAll("td");
    const collection = cells[0]?.textContent || "";
    const tokenId = cells[1]?.textContent || "";
    if (collection && tokenId) {
      assetLines.push(`• ${collection} #${tokenId}`);
    }
  });
  
  const today = new Date().toLocaleDateString();
  
  // Build wallets list
  let walletsList = `<div class="wallet-box"><strong>Primary Wallet:</strong> ${primaryWalletAddress}</div>`;
  if (additionalWallets.length > 0) {
    walletsList += `<div class="wallet-box"><strong>Additional Wallets:</strong><ul>`;
    additionalWallets.forEach(wallet => {
      walletsList += `<li>${wallet.address}${wallet.ens ? ` (${wallet.ens})` : ""}</li>`;
    });
    walletsList += `</ul></div>`;
  }
  
  // Build asset distribution
  let assetDistribution = "";
  if (beneficiaries.length > 0) {
    assetDistribution = beneficiaries.map(b => 
      `<p><strong>${b.name}</strong>${b.ens ? ` (${b.ens})` : ""}: To receive designated percentage of digital assets as specified in assignment records.</p>`
    ).join("");
  } else {
    assetDistribution = "<p>Beneficiaries to be designated through assignment records.</p>";
  }
  
  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Last Will and Testament of ${ownerFullName}</title>
  <style>
    body { font-family: 'Times New Roman', serif; line-height: 1.6; margin: 40px; color: #000; background: #fff; }
    .header { text-align: center; margin-bottom: 40px; }
    .header h1 { font-size: 24px; font-weight: bold; margin: 0; text-decoration: underline; }
    .article { margin: 30px 0; }
    .article h2 { font-size: 16px; font-weight: bold; text-decoration: underline; margin: 20px 0 10px 0; }
    .article h3 { font-size: 14px; font-weight: bold; margin: 15px 0 5px 0; }
    .wallet-box { border: 2px solid #000; padding: 10px; margin: 10px 0; }
    .asset-list { margin: 15px 0; }
    .signature-section { margin-top: 50px; }
    .signature-line { border-bottom: 1px solid #000; width: 300px; height: 20px; margin: 20px 0; }
    .witness-section { margin-top: 40px; display: flex; justify-content: space-between; }
    .witness-box { width: 45%; }
    .notary-section { margin-top: 40px; border: 2px solid #000; padding: 20px; }
    .notary-seal { border: 2px solid #000; width: 150px; height: 100px; float: right; margin: 20px; text-align: center; padding: 20px; }
    .date-line { border-bottom: 1px solid #000; display: inline-block; width: 150px; height: 20px; }
    ul { margin: 10px 0; padding-left: 20px; }
    p { margin: 10px 0; text-align: justify; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Last Will and Testament of ${ownerFullName}</h1>
  </div>

  <div class="article">
    <h2>ARTICLE I - DECLARATION AND REVOCATION</h2>
    <p>I, <strong>${ownerFullName}</strong>, a resident of the jurisdiction where this will is executed, being of sound mind and memory and not acting under duress, menace, fraud, or undue influence of any person whomsoever, do hereby make, publish, and declare this instrument to be my Last Will and Testament, hereby expressly revoking all wills and codicils heretofore made by me.</p>
    
    <p>I am over the age of eighteen (18) years and am competent to make this Will. I declare that this Will expresses my true wishes concerning the disposition of my digital assets and that I have carefully read this Will and understand its contents.</p>
  </div>

  <div class="article">
    <h2>ARTICLE II - DIGITAL ASSET IDENTIFICATION AND DISPOSITION</h2>
    <p>I hereby give, devise, and bequeath all of my right, title, and interest in and to my digital assets, including but not limited to cryptocurrency, digital tokens, non-fungible tokens (NFTs), smart contracts, and other blockchain-based assets, currently held in or accessible through the following digital wallet addresses:</p>
    
    ${walletsList}
    
    <p><strong>Current Digital Asset Inventory (as of ${today}):</strong></p>
    <div class="asset-list">
      ${assetLines.length > 0 ? assetLines.map(line => `<p>${line}</p>`).join("") : "<p>• Digital assets to be inventoried at time of distribution</p>"}
    </div>
    
    <p><strong>Total Estimated Portfolio Value:</strong> To be determined at time of distribution</p>
    
    <h3>Asset Distribution:</h3>
    ${assetDistribution}
  </div>

  <div class="article">
    <h2>ARTICLE III - APPOINTMENT OF EXECUTOR AND DIGITAL ASSET POWERS</h2>
    <p>I hereby nominate, constitute, and appoint <strong>${primaryExecutor ? primaryExecutor.name : "To be designated"}</strong> as the Executor of this Last Will and Testament. If ${primaryExecutor ? primaryExecutor.name : "the primary executor"} is unable, unwilling, or fails to qualify as Executor, I nominate and appoint <strong>${backupExecutor ? backupExecutor.name : "To be designated"}</strong> as successor Executor.</p>
    
    <p><strong>Digital Asset Authority:</strong> I specifically grant my Executor the following powers and authorities with respect to my digital assets:</p>
    
    <p>a) To locate, access, and take control of all digital wallets, private keys, seed phrases, passwords, and authentication methods necessary to access my digital assets;</p>
    
    <p>b) To engage qualified blockchain technology experts, cryptocurrency services, or digital asset custodians as necessary;</p>
    
    <p>c) To convert digital assets to fiat currency if required for estate settlement or tax obligations;</p>
    
    <p>d) To create new digital wallets and transfer assets to beneficiaries' designated addresses;</p>
    
    <p>e) To claim any forks, airdrops, staking rewards, or other derivative benefits;</p>
    
    <p>f) To pay all taxes, fees, and expenses related to digital asset management and transfer;</p>
    
    <p>g) To execute all necessary documents and transactions to effectuate the distribution of digital assets.</p>
  </div>

  <div class="article">
    <h2>ARTICLE IV - DIGITAL ASSET ADMINISTRATION INSTRUCTIONS</h2>
    <p><strong>Immediate Actions Required:</strong></p>
    
    <p><strong>1. Security:</strong> My Executor shall immediately secure all digital assets by obtaining control of private keys and changing passwords to prevent unauthorized access;</p>
    
    <p><strong>2. Inventory:</strong> Conduct a complete inventory and valuation of all digital assets within thirty (30) days of my death;</p>
    
    <p><strong>3. Documentation:</strong> Maintain detailed records of all digital asset transactions, including blockchain transaction IDs;</p>
    
    <p><strong>4. Distribution:</strong> Transfer assets to beneficiaries within ninety (90) days unless additional time is required for tax or legal compliance;</p>
    
    <p><strong>5. Tax Compliance:</strong> Ensure all federal, state, and local tax obligations are satisfied before final distribution.</p>
    
    ${specialInstructionsText ? `<p><strong>SPECIAL INSTRUCTIONS AND ADDITIONAL WISHES:</strong></p><div style="border: 1px solid #000; padding: 15px; margin: 15px 0; font-style: italic;">"${specialInstructionsText}"</div><p>I direct my Executor to carefully consider and implement these additional instructions to the extent legally permissible and practically feasible. These instructions are an integral part of my wishes for the administration of my digital assets.</p>` : ""}
  </div>

  <div class="article">
    <h2>ARTICLE V - GENERAL PROVISIONS AND GOVERNING LAW</h2>
    <p><strong>Governing Law:</strong> This Will shall be construed and administered according to the laws of the state of my domicile at the time of my death, without regard to conflict of laws principles.</p>
    
    <p><strong>Severability:</strong> If any provision of this Will is held to be invalid or unenforceable, such determination shall not affect the validity or enforceability of the remaining provisions, which shall continue in full force and effect.</p>
    
    <p><strong>Digital Asset Definition:</strong> "Digital assets" as used herein includes cryptocurrency, virtual currency, digital tokens, non-fungible tokens (NFTs), blockchain-based assets, smart contracts, and any other form of digital property that exists on a blockchain or distributed ledger.</p>
  </div>

  <div class="signature-section">
    <p><strong>IN WITNESS WHEREOF,</strong> I have signed my name to this Last Will and Testament this _____ day of _____________, 20____.</p>
    
    <div style="margin-top: 40px;">
      <p><strong>TESTATOR:</strong></p>
      <div class="signature-line"></div>
      <p style="text-align: center;"><strong>${ownerFullName}</strong></p>
      <p style="text-align: center;">(Signature)</p>
    </div>
  </div>

  <div class="article">
    <h2>ATTESTATION OF WITNESSES</h2>
    <p>Each of us declares under penalty of perjury that the following is true and correct:</p>
    
    <p>a) The testator signed this Will in our presence;</p>
    <p>b) The testator appeared to be of sound mind and under no duress;</p>
    <p>c) We signed as witnesses in the testator's presence and in each other's presence;</p>
    <p>d) Each of us is over 18 years of age;</p>
    <p>e) Neither of us is a beneficiary of this Will.</p>
    
    <div class="witness-section">
      <div class="witness-box">
        <p><strong>WITNESS 1:</strong></p>
        <div class="signature-line"></div>
        <p><strong>Batman</strong></p>
        <p>(Print Name)</p>
        <div class="signature-line"></div>
        <p>(Signature)</p>
        <div class="signature-line"></div>
        <p>(Address)</p>
        <p>Date: _______________</p>
      </div>
      
      <div class="witness-box">
        <p><strong>WITNESS 2:</strong></p>
        <div class="signature-line"></div>
        <p><strong>Locie</strong></p>
        <p>(Print Name)</p>
        <div class="signature-line"></div>
        <p>(Signature)</p>
        <div class="signature-line"></div>
        <p>(Address)</p>
        <p>Date: _______________</p>
      </div>
    </div>
  </div>

  <div class="notary-section">
    <h2>NOTARIAL ACKNOWLEDGMENT</h2>
    <p><strong>State of:</strong> <span class="date-line"></span></p>
    <p><strong>County of:</strong> <span class="date-line"></span></p>
    
    <p>On this <span class="date-line"></span> day of <span class="date-line"></span>, 20<span class="date-line"></span>, before me personally appeared <strong>${ownerFullName}</strong>, who proved to me on the basis of satisfactory evidence to be the person whose name is subscribed to the within instrument and acknowledged to me that he/she executed the same in his/her authorized capacity.</p>
    
    <p>I certify under <strong>PENALTY OF PERJURY</strong> under the laws of the State of <span class="date-line"></span> that the foregoing paragraph is true and correct.</p>
    
    <div style="margin-top: 40px;">
      <div class="signature-line" style="margin: 0 auto;"></div>
      <p style="text-align: center;">(Signature of Notary Public)</p>
      
      <div class="notary-seal">
        <div>
          <strong>NOTARY SEAL</strong><br>
          <small>(Affix Official Seal Above)</small>
        </div>
      </div>
      
      <p><strong>My commission expires:</strong> <span class="date-line"></span></p>
    </div>
  </div>
  
</body>
</html>`;

  // Better mobile solution - create modal overlay instead of new window
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  
  if (isMobile) {
    // Create modal overlay for mobile
    const modal = document.createElement('div');
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.9);
      z-index: 10000;
      overflow-y: auto;
      padding: 20px;
      box-sizing: border-box;
    `;
    
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕ Close';
    closeBtn.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: #1d9bf0;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 20px;
      font-size: 16px;
      cursor: pointer;
      z-index: 10001;
    `;
    closeBtn.onclick = () => document.body.removeChild(modal);
    
    const printBtn = document.createElement('button');
    printBtn.innerHTML = '🖨️ Print';
    printBtn.style.cssText = `
      position: fixed;
      top: 10px;
      right: 100px;
      background: #00ba7c;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 20px;
      font-size: 16px;
      cursor: pointer;
      z-index: 10001;
    `;
    printBtn.onclick = () => window.print();
    
    const content = document.createElement('div');
    content.innerHTML = html;
    content.style.cssText = `
      background: white;
      color: black;
      padding: 20px;
      border-radius: 8px;
      max-width: 800px;
      margin: 60px auto 20px;
      font-family: 'Times New Roman', serif;
      line-height: 1.6;
    `;
    
    modal.appendChild(closeBtn);
    modal.appendChild(printBtn);
    modal.appendChild(content);
    document.body.appendChild(modal);
    
  } else {
    // Desktop solution - original method
    const w = window.open("", "_blank");
    if (w) {
      w.document.open();
      w.document.write(html);
      w.document.close();
    } else {
      // Fallback if popup blocked
      alert('Popup blocked. Please allow popups for this site and try again.');
    }
  }
}

// Make handlePrint globally accessible
window.handlePrint = handlePrint;

// Add event listener for the print button
document.addEventListener('DOMContentLoaded', function() {
  const printButton = document.getElementById('btnPrint');
  if (printButton) {
    printButton.addEventListener('click', handlePrint);
  }
});