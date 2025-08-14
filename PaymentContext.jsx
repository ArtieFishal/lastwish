import React, { createContext, useContext, useState } from 'react';
import { toast } from 'sonner';

const PaymentContext = createContext({});

export function PaymentProvider({ children }) {
  const [paymentStatus, setPaymentStatus] = useState('pending'); // pending, processing, completed, failed
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [hasPaid, setHasPaid] = useState(false);

  // Simulate payment processing
  const processPayment = (plan) => {
    setPaymentStatus('processing');
    setSelectedPlan(plan);

    toast.info('Processing payment...');

    setTimeout(() => {
      setPaymentStatus('completed');
      setHasPaid(true);
      toast.success('Payment successful!');
    }, 3000);
  };

  const value = {
    paymentStatus,
    selectedPlan,
    hasPaid,
    processPayment,
  };

  return (
    <PaymentContext.Provider value={value}>
      {children}
    </PaymentContext.Provider>
  );
}

export const usePayment = () => {
  const context = useContext(PaymentContext);
  if (!context) {
    throw new Error('usePayment must be used within a PaymentProvider');
  }
  return context;
};
