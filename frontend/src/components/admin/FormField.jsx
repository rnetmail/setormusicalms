import { forwardRef } from 'react';

const FormField = forwardRef(({ 
  label, 
  name, 
  type = 'text',
  placeholder = '',
  required = false,
  error = '',
  options = [],
  value = '',
  onChange,
  className = '',
  ...props 
}, ref) => {
  
  let inputElement;
  
  if (type === 'textarea') {
    inputElement = (
      <textarea
        id={name}
        name={name}
        ref={ref}
        className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 ${className} ${error ? 'border-red-500' : ''}`}
        placeholder={placeholder}
        required={required}
        value={value}
        onChange={onChange}
        {...props}
      />
    );
  } else if (type === 'select') {
    inputElement = (
      <select
        id={name}
        name={name}
        ref={ref}
        className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 ${className} ${error ? 'border-red-500' : ''}`}
        required={required}
        value={value}
        onChange={onChange}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    );
  } else {
    inputElement = (
      <input
        id={name}
        name={name}
        type={type}
        ref={ref}
        className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 ${className} ${error ? 'border-red-500' : ''}`}
        placeholder={placeholder}
        required={required}
        value={value}
        onChange={onChange}
        {...props}
      />
    );
  }

  return (
    <div className="mb-4">
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      {inputElement}
      {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
    </div>
  );
});

FormField.displayName = 'FormField';

export default FormField;