import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { formatUnits } from 'viem';
import FormField from './FormField';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useFieldArray } from "react-hook-form";
import { useAccount, useBalance, usePublicClient } from 'wagmi';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { ERC20_ABI, ERC20_TOKENS } from '@/lib/constants';
import { alchemy } from '@/lib/alchemy';


// --- Reusable Validation ---
const noSensitiveData = (zodString) => {
  return zodString.refine(value => {
    if (!value) return true; // Allow empty/optional strings
    const sensitiveRegex = /(?:\b[a-zA-Z]+\b\s*){11,}/;
    return !sensitiveRegex.test(value);
  }, { message: "Do not enter seed phrases or other sensitive data." });
};

// --- Schemas ---
const assetSchema = z.object({
  assetType: z.string().min(1, { message: "Required" }),
  platform: z.string().min(1, { message: "Required" }),
  network: z.string().min(1, { message: "Required" }),
  notes: noSensitiveData(z.string().optional()),
  url: noSensitiveData(z.string().url({ message: "Invalid URL" }).optional().or(z.literal(''))),
  physicalLocation: noSensitiveData(z.string().optional()),
  verified: z.boolean().optional(),
  image: z.string().url().optional(),
});

const beneficiarySchema = z.object({
  name: noSensitiveData(z.string().min(2, { message: "Name must be at least 2 characters." })),
  relationship: noSensitiveData(z.string().optional()),
  allocation: z.coerce.number().min(1, { message: "Min 1%" }).max(100, { message: "Max 100%" }),
});

const assetTypes = ["Fungible Token", "NFT", "DeFi Position", "Other"];
const platforms = ["Coinbase", "MetaMask", "Ledger", "Trezor", "Other"];
const networks = ["Ethereum", "Polygon", "BSC", "Avalanche", "Bitcoin", "Solana", "Other"];

// Define the validation schema for the entire form.
const formSchema = z.object({
  personalInfo: z.object({
    fullName: noSensitiveData(z.string().min(2, { message: "Full name must be at least 2 characters." })),
    dateOfBirth: z.string().refine((val) => !isNaN(Date.parse(val)), { message: "Please enter a valid date." }),
    address: noSensitiveData(z.string().min(10, { message: "Address must be at least 10 characters." })),
  }),
  executorDetails: z.object({
    primaryExecutorName: noSensitiveData(z.string().min(2, { message: "Name must be at least 2 characters." })),
    primaryExecutorEmail: z.string().email({ message: "Please enter a valid email." }),
    backupExecutorName: noSensitiveData(z.string().min(2, { message: "Name must be at least 2 characters." }).optional().or(z.literal(''))),
    backupExecutorEmail: z.string().email({ message: "Please enter a valid email." }).optional().or(z.literal('')),
  }),
  beneficiaries: z.array(beneficiarySchema),
  assets: z.array(assetSchema),
}).refine(data => {
  if (data.beneficiaries.length === 0) return true;
  const totalAllocation = data.beneficiaries.reduce((acc, b) => acc + b.allocation, 0);
  return totalAllocation === 100;
}, {
  message: "Total allocation for all beneficiaries must be exactly 100%",
  path: ["beneficiaries"],
});

const GuideForm = () => {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      personalInfo: { fullName: "", dateOfBirth: "", address: "" },
      executorDetails: { primaryExecutorName: "", primaryExecutorEmail: "", backupExecutorName: "", backupExecutorEmail: "" },
      beneficiaries: [],
      assets: [],
    },
  });

  const { fields: beneficiaryFields, append: appendBeneficiary, remove: removeBeneficiary } = useFieldArray({ name: "beneficiaries", control: form.control });
  const { fields: assetFields, append: appendAsset, remove: removeAsset } = useFieldArray({ name: "assets", control: form.control });

  const { address, isConnected, chain } = useAccount();
  const { data: balanceData } = useBalance({ address });
  const publicClient = usePublicClient();

  const handleFetchAssets = async () => {
    if (!isConnected || !address || !chain) return;

    // 1. Fetch native balance
    if (balanceData) {
      appendAsset({
        assetType: "Fungible Token",
        platform: "Wallet",
        network: chain.name,
        notes: `Native balance: ${balanceData.formatted} ${balanceData.symbol}`,
        verified: true,
        url: '', physicalLocation: ''
      });
    }

    // 2. Fetch ERC20 balances
    const tokensForChain = ERC20_TOKENS[chain.id];
    if (tokensForChain && tokensForChain.length > 0) {
      const contracts = tokensForChain.map(token => ({
        address: token.address,
        abi: ERC20_ABI,
        functionName: 'balanceOf',
        args: [address],
      }));

      try {
        const results = await publicClient.multicall({ contracts });
        results.forEach((result, index) => {
          if (result.status === 'success' && result.result > 0) {
            const token = tokensForChain[index];
            const formattedBalance = formatUnits(result.result, token.decimals);
            appendAsset({
              assetType: "Fungible Token",
              platform: "Wallet",
              network: chain.name,
              notes: `Token: ${token.name} (${token.symbol}), Balance: ${formattedBalance}`,
              verified: true,
              url: `https://etherscan.io/token/${token.address}`,
              physicalLocation: '',
            });
          }
        });
      } catch (error) {
        console.error("Error fetching ERC20 balances:", error);
      }
    }

    // 3. Fetch NFTs
    try {
      const nfts = await alchemy.nft.getNftsForOwner(address);
      nfts.ownedNfts.forEach(nft => {
        appendAsset({
          assetType: "NFT",
          platform: "Wallet",
          network: chain.name,
          notes: `NFT: ${nft.name || 'Unnamed NFT'} (ID: ${nft.tokenId})`,
          verified: true,
          url: `https://etherscan.io/token/${nft.contract.address}?a=${nft.tokenId}`,
          physicalLocation: '',
          image: nft.media[0]?.thumbnail || '',
        });
      });
    } catch (error) {
      console.error("Error fetching NFTs:", error);
    }
  };

  const [hasDraft, setHasDraft] = useState(false);

  useEffect(() => {
    const savedDraft = localStorage.getItem('lastwish-draft');
    if (savedDraft) {
      setHasDraft(true);
    }
  }, []);

  const handleLoadDraft = () => {
    const savedDraft = localStorage.getItem('lastwish-draft');
    if (savedDraft) {
      const draftValues = JSON.parse(savedDraft);
      form.reset(draftValues);
      alert('Draft loaded!');
    }
  };

  const onSubmit = (data) => {
    console.log("Form submitted successfully!");
    console.log(data);
  };

  const handleSaveDraft = () => {
    const formValues = form.getValues();
    localStorage.setItem('lastwish-draft', JSON.stringify(formValues));
    alert('Draft saved!');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-white">Guide Creation Form</h2>
        {hasDraft && (
          <Button type="button" variant="outline" onClick={handleLoadDraft}>
            Load Saved Draft
          </Button>
        )}
      </div>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        {/* Cards for Personal Info, Executor, Beneficiaries */}
        <Card>
          <CardHeader><CardTitle>Personal Information</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <FormField label="Full Legal Name" id="fullName" type="text" register={form.register('personalInfo.fullName')} error={form.formState.errors.personalInfo?.fullName} placeholder="John Doe"/>
            <FormField label="Date of Birth" id="dateOfBirth" type="date" register={form.register('personalInfo.dateOfBirth')} error={form.formState.errors.personalInfo?.dateOfBirth}/>
            <FormField label="Full Mailing Address" id="address" type="text" register={form.register('personalInfo.address')} error={form.formState.errors.personalInfo?.address} placeholder="123 Main St, Anytown, USA 12345"/>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Executor Details</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <h4 className="font-semibold text-gray-300">Primary Executor</h4>
            <FormField label="Full Legal Name" id="primaryExecutorName" type="text" register={form.register('executorDetails.primaryExecutorName')} error={form.formState.errors.executorDetails?.primaryExecutorName} placeholder="Jane Smith"/>
            <FormField label="Email Address" id="primaryExecutorEmail" type="email" register={form.register('executorDetails.primaryExecutorEmail')} error={form.formState.errors.executorDetails?.primaryExecutorEmail} placeholder="jane.smith@example.com"/>
            <h4 className="font-semibold text-gray-300 pt-4">Backup Executor (Optional)</h4>
            <FormField label="Full Legal Name" id="backupExecutorName" type="text" register={form.register('executorDetails.backupExecutorName')} error={form.formState.errors.executorDetails?.backupExecutorName} placeholder="Sam Jones"/>
            <FormField label="Email Address" id="backupExecutorEmail" type="email" register={form.register('executorDetails.backupExecutorEmail')} error={form.formState.errors.executorDetails?.backupExecutorEmail} placeholder="sam.jones@example.com"/>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Beneficiaries</CardTitle></CardHeader>
          <CardContent className="space-y-6">
            <div>
              {beneficiaryFields.map((field, index) => (
                <div key={field.id} className="flex items-center space-x-4 p-3 bg-gray-700/40 rounded-md mb-2">
                  <div className="grid grid-cols-3 gap-4 flex-grow">
                    <FormField label="Beneficiary Name" id={`beneficiary-name-${index}`} register={form.register(`beneficiaries.${index}.name`)} error={form.formState.errors.beneficiaries?.[index]?.name} placeholder="Alice"/>
                    <FormField label="Relationship (Optional)" id={`beneficiary-relationship-${index}`} register={form.register(`beneficiaries.${index}.relationship`)} error={form.formState.errors.beneficiaries?.[index]?.relationship} placeholder="Spouse"/>
                    <FormField label="Allocation (%)" id={`beneficiary-allocation-${index}`} type="number" register={form.register(`beneficiaries.${index}.allocation`)} error={form.formState.errors.beneficiaries?.[index]?.allocation} placeholder="50"/>
                  </div>
                  <Button type="button" variant="destructive" size="sm" onClick={() => removeBeneficiary(index)}>Remove</Button>
                </div>
              ))}
            </div>
            <Button type="button" variant="outline" onClick={() => appendBeneficiary({ name: '', relationship: '', allocation: 0 })}>Add Beneficiary</Button>
            {form.formState.errors.beneficiaries && (<p className="mt-2 text-sm text-red-500">{form.formState.errors.beneficiaries.message}</p>)}
          </CardContent>
        </Card>

        {/* Asset Discovery Card */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Asset Discovery</CardTitle>
            <Button type="button" onClick={handleFetchAssets} disabled={!isConnected}>Fetch Assets</Button>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              {assetFields.map((field, index) => {
                const asset = form.getValues(`assets.${index}`);
                return (
                  <div key={field.id} className="space-y-4 p-4 bg-gray-700/40 rounded-md mb-4 relative">
                    {asset.verified && <Badge className="absolute top-2 right-2">Verified</Badge>}
                    <div className="flex items-start space-x-4">
                      {asset.image && <img src={asset.image} alt="NFT" className="w-24 h-24 rounded-md object-cover" />}
                      <div className="flex-grow space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <FormField label="Asset Type" id={`asset-type-${index}`} error={form.formState.errors.assets?.[index]?.assetType}><Select onValueChange={(value) => form.setValue(`assets.${index}.assetType`, value)} defaultValue={asset.assetType}><SelectTrigger><SelectValue placeholder="Select asset type" /></SelectTrigger><SelectContent>{assetTypes.map(type => <SelectItem key={type} value={type}>{type}</SelectItem>)}</SelectContent></Select></FormField>
                          <FormField label="Platform / Wallet" id={`asset-platform-${index}`} error={form.formState.errors.assets?.[index]?.platform}><Select onValueChange={(value) => form.setValue(`assets.${index}.platform`, value)} defaultValue={asset.platform}><SelectTrigger><SelectValue placeholder="Select platform" /></SelectTrigger><SelectContent>{platforms.map(p => <SelectItem key={p} value={p}>{p}</SelectItem>)}</SelectContent></Select></FormField>
                          <FormField label="Network" id={`asset-network-${index}`} error={form.formState.errors.assets?.[index]?.network}><Select onValueChange={(value) => form.setValue(`assets.${index}.network`, value)} defaultValue={asset.network}><SelectTrigger><SelectValue placeholder="Select network" /></SelectTrigger><SelectContent>{networks.map(n => <SelectItem key={n} value={n}>{n}</SelectItem>)}</SelectContent></Select></FormField>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <FormField label="URL / Public Address (Optional)" id={`asset-url-${index}`} type="text" register={form.register(`assets.${index}.url`)} error={form.formState.errors.assets?.[index]?.url} placeholder="https://etherscan.io/address/0x..."/>
                          <FormField label="Physical Location (Optional)" id={`asset-location-${index}`} type="text" register={form.register(`assets.${index}.physicalLocation`)} error={form.formState.errors.assets?.[index]?.physicalLocation} placeholder="Safe deposit box #123"/>
                        </div>
                        <FormField label="Notes (Optional)" id={`asset-notes-${index}`} type="text" register={form.register(`assets.${index}.notes`)} error={form.formState.errors.assets?.[index]?.notes} placeholder="Notes for your executor..."/>
                        <Button type="button" variant="destructive" size="sm" onClick={() => removeAsset(index)}>Remove Asset</Button>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
            <Button type="button" variant="outline" onClick={() => appendAsset({ assetType: '', platform: '', network: '', url: '', physicalLocation: '', notes: '', verified: false, image: '' })}>Add Asset Manually</Button>
          </CardContent>
        </Card>

        <div className="flex space-x-4">
          <Button type="button" variant="secondary" className="w-full" onClick={handleSaveDraft}>
            Save Draft
          </Button>
          <Button type="submit" className="w-full">
            Save & Continue
          </Button>
        </div>
      </form>
    </div>
  );
};

export default GuideForm;
