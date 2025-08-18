import jsPDF from 'jspdf';
import 'jspdf-autotable'; // Even if not used directly, it can extend jsPDF

/**
 * Generates a PDF document from the form data.
 * @param {object} formData - The validated data from the form.
 */
export function generatePdf(formData) {
  const doc = new jsPDF();
  let y = 15; // Initial Y position

  // --- Helper Functions ---
  const checkPageBreak = () => {
    if (y > 280) { // Check if Y position is close to the bottom
      doc.addPage();
      y = 15; // Reset Y position for new page
    }
  };

  const addTitle = (title) => {
    checkPageBreak();
    doc.setFont('times', 'bold');
    doc.setFontSize(16);
    doc.text(title, 14, y);
    y += 10;
    doc.setLineWidth(0.5);
    doc.line(14, y - 5, 196, y - 5);
  };

  const addSection = (title, data) => {
    addTitle(title);
    doc.setFont('times', 'normal');
    doc.setFontSize(12);
    Object.entries(data).forEach(([key, value]) => {
      if (value) {
        checkPageBreak();
        const formattedKey = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
        doc.text(`${formattedKey}:`, 14, y);
        doc.text(String(value), 70, y);
        y += 7;
      }
    });
    y += 5; // Add some space after the section
  };

  // --- PDF Content ---

  // Title Page
  doc.setFont('times', 'bold');
  doc.setFontSize(22);
  doc.text('LastWish.eth', 105, 60, null, null, 'center');
  doc.setFontSize(16);
  doc.text('Digital Asset Estate Planning Addendum', 105, 70, null, null, 'center');
  doc.setFont('times', 'normal');
  doc.setFontSize(12);
  doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 105, 80, null, null, 'center');


  // Personal Info
  doc.addPage();
  y = 15;
  addSection('Personal Information', formData.personalInfo);

  // Executor Details
  addSection('Executor Details', {
    'Primary Executor Name': formData.executorDetails.primaryExecutorName,
    'Primary Executor Email': formData.executorDetails.primaryExecutorEmail,
    'Backup Executor Name': formData.executorDetails.backupExecutorName,
    'Backup Executor Email': formData.executorDetails.backupExecutorEmail,
  });

  // Beneficiaries
  if (formData.beneficiaries && formData.beneficiaries.length > 0) {
    addTitle('Beneficiaries');
    formData.beneficiaries.forEach((b, i) => {
      addSection(`Beneficiary #${i + 1}`, {
        'Name': b.name,
        'Relationship': b.relationship,
        'Allocation (%)': b.allocation,
      });
    });
  }

  // Assets
  if (formData.assets && formData.assets.length > 0) {
    addTitle('Asset Discovery Guide');
    formData.assets.forEach((a, i) => {
      addSection(`Asset #${i + 1}`, {
        'Asset Type': a.assetType,
        'Platform / Wallet': a.platform,
        'Network': a.network,
        'URL / Public Address': a.url,
        'Physical Location': a.physicalLocation,
        'Notes': a.notes,
        'Verified by App': a.verified ? 'Yes' : 'No',
      });
    });
  }

  // Legal Disclaimer
  doc.addPage();
  y = 15;
  addTitle('Legal Disclaimer & Guidance');
  doc.setFont('times', 'normal');
  doc.setFontSize(10);
  const disclaimer = `
    This document is an addendum to my formal will or trust and serves as a guide for my executor to locate and access my digital assets. It is not a substitute for a legal will.
    I affirm that the information contained herein is accurate to the best of my knowledge.

    This document is intended to be compliant with the Revised Uniform Fiduciary Access to Digital Assets Act (RUFADAA) and the Uniform Probate Code.
    It is strongly recommended that my executor consult with a legal professional and a tax advisor specializing in digital assets.

    IMPORTANT: This guide intentionally does NOT contain any private keys, seed phrases, or passwords. These credentials are stored separately in a secure, offline location as described in a separate memorandum.
  `;
  const splitDisclaimer = doc.splitTextToSize(disclaimer, 180);
  doc.text(splitDisclaimer, 14, y);
  y += (splitDisclaimer.length * 4) + 10;

  // Notary Block
  checkPageBreak();
  addTitle('Notarization');
  y += 20;
  doc.text('State of ________________________', 14, y);
  y += 10;
  doc.text('County of _______________________', 14, y);
  y += 20;
  doc.text('On this ______ day of _______________, 20____, before me, the undersigned notary public,', 14, y);
  y += 7;
  doc.text('personally appeared ____________________________________, known to me (or satisfactorily proven)', 14, y);
  y += 7;
  doc.text('to be the person whose name is subscribed to the within instrument, and acknowledged that', 14, y);
  y += 7;
  doc.text('he/she executed the same for the purposes therein contained.', 14, y);
  y += 20;
  doc.text('____________________________________', 14, y);
  y += 7;
  doc.text('Notary Public', 14, y);
  y += 10;
  doc.text('My Commission Expires: ______________', 14, y);

  doc.save('lastwish-guide.pdf');
}
