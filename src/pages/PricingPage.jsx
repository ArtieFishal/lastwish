import React from 'react';
import { useSendTransaction, useWaitForTransactionReceipt } from 'wagmi';
import { parseEther } from 'viem';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

const PricingPage = () => {
  const { data: hash, isPending, sendTransaction } = useSendTransaction();

  const { isLoading: isConfirming, isSuccess: isConfirmed } =
    useWaitForTransactionReceipt({
      hash,
    });

  const handlePayment = () => {
    sendTransaction({
      to: '0x016ae25Ac494B123C40EDb2418d9b1FC2d62279b',
      value: parseEther('0.00001'),
    });
  };

  return (
    <div className="container mx-auto py-12 flex justify-center">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl">Create Your Guide</CardTitle>
          <CardDescription className="pt-2">
            A one-time payment is required to generate your notarizable PDF guide.
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-5xl font-bold">0.00001 ETH</p>
          <p className="text-sm text-gray-400 mt-2">(For testing purposes)</p>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button className="w-full" onClick={handlePayment} disabled={isPending || isConfirming}>
            {isPending ? 'Confirm in wallet...' : isConfirming ? 'Processing Payment...' : 'Proceed to Payment'}
          </Button>

          {hash && <div className="text-xs text-center break-all">Transaction Hash: {hash}</div>}

          {isConfirming && <div className="text-sm text-center text-yellow-400">Waiting for confirmation...</div>}

          {isConfirmed && <div className="text-sm text-center text-green-400">Payment successful!</div>}

          <p className="text-center text-xs text-gray-500">
            Payments may trigger capital gains; consult a tax professional.
          </p>
        </CardFooter>
      </Card>
    </div>
  );
};

export default PricingPage;
