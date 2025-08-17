import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { generatePdf } from '@/lib/pdfGenerator';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

const DownloadPage = () => {
  const [isPaid, setIsPaid] = useState(false);
  const [draftExists, setDraftExists] = useState(false);

  useEffect(() => {
    // In a real app, we'd have a more secure way to check this.
    // For now, we'll simulate it by checking a value in localStorage.
    // I will add the logic to set this after payment confirmation later.
    const paymentStatus = localStorage.getItem('paymentConfirmed') === 'true';
    setIsPaid(paymentStatus);

    const savedDraft = localStorage.getItem('lastwish-draft');
    setDraftExists(!!savedDraft);
  }, []);

  const handleDownload = () => {
    const savedDraft = localStorage.getItem('lastwish-draft');
    if (savedDraft) {
      const formData = JSON.parse(savedDraft);
      generatePdf(formData);
    } else {
      alert("No saved draft found. Please create and save a guide first.");
    }
  };

  return (
    <div className="container mx-auto py-12 flex justify-center">
      <Card className="w-full max-w-lg text-center">
        <CardHeader>
          <CardTitle className="text-3xl">Download Your Guide</CardTitle>
          <CardDescription className="pt-2">
            Your printable PDF guide is ready for download.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isPaid && draftExists ? (
            <div>
              <p className="mb-6">Your payment has been confirmed. You can now download your PDF. Store it in a safe place and inform your executor of its location.</p>
              <Button onClick={handleDownload} className="w-full">
                Download PDF
              </Button>
            </div>
          ) : !draftExists ? (
            <p className="text-yellow-400">Please create and save a draft on the 'Create Guide' page before you can download.</p>
          ) : (
            <p className="text-red-500">Payment has not been confirmed. Please complete the payment on the 'Pricing' page to enable download.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default DownloadPage;
