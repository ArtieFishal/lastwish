import React from 'react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

const FormField = ({ children, label, id, error, register, ...props }) => {
  return (
    <div className="grid w-full items-center gap-1.5">
      <Label htmlFor={id}>{label}</Label>
      {children ? (
        React.cloneElement(children, { id })
      ) : (
        <Input
          id={id}
          {...register}
          {...props}
          className={error ? 'border-red-500' : ''}
        />
      )}
      {error && <p className="mt-2 text-sm text-red-500">{error.message}</p>}
    </div>
  );
};

export default FormField;
