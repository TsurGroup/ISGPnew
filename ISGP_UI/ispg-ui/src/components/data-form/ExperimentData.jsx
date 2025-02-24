

import { FormProvider } from '../../contexts/FormContext';

import DataForm from './DataForm.jsx';



const ExperimentData = () => {


const initialExperimentDataForm = {
    file1: null,
    file2: null,
    w0: 0.001,
    w1: 0.001,
    useFilter: false,
  };


  return (

      <FormProvider initialFormData={initialExperimentDataForm}>
        <DataForm/>
      </FormProvider>
  );
};

export default ExperimentData;

