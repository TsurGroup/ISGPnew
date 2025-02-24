import React, { createContext, useContext, useState } from 'react';

const FormContext = createContext();

export const useForm = () => useContext(FormContext);

export const FormProvider = ({ children, initialFormData }) => {
  const [formData, setFormData] = useState(initialFormData);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleListChange = (fieldName, index) => {
    setFormData((prevData) => {
      const currentList = prevData[fieldName] || [];
      const newCheckedIndices = currentList.includes(index)
        ? currentList.filter((i) => i !== index)
        : [...currentList, index];

      return {
        ...prevData,
        [fieldName]: newCheckedIndices,
      };
    });
  };

  const handleDictChange = (fieldName, key, value) => {
    setFormData((prevData) => {
      const updatedDict = { ...prevData[fieldName], [key]: value };
      return {
        ...prevData,
        [fieldName]: updatedDict,
      };
    });
  };

const handleFileChange = (e) => {
    const { name, files } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: Array.from(files), // Store the selected files as an array
    }));
  };

  return (
    <FormContext.Provider value={{ formData, handleChange, handleFileChange, handleListChange, handleDictChange,setFormData }}>
      {children}
    </FormContext.Provider>
  );
};
