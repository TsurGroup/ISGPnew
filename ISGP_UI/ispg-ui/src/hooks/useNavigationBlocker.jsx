import { useEffect, useState } from 'react';

const useNavigationBlocker = () => {
  const [open, setOpen] = useState(false);
  
  useEffect(() => {
    const handleBeforeUnload = (event) => {
      event.preventDefault();
      event.returnValue = ''; // Show browser's default confirmation
    };

    const handleBackButton = (event) => {
      event.preventDefault();
      setOpen(true); // Open the custom dialog
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    window.history.pushState(null, '', window.location.href);
    window.addEventListener('popstate', handleBackButton);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      window.removeEventListener('popstate', handleBackButton);
    };
  }, []);

  return [open, setOpen]; // Return the open state and the setter
};

export default useNavigationBlocker;
