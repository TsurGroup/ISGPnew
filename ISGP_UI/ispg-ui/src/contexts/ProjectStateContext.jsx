import React, { createContext, useContext, useState } from 'react';

// Create Context
const ProjectStateContext = createContext();
const ProjectStateUpdateContext = createContext();

// Custom hooks for accessing context
export const useProjectState = () => useContext(ProjectStateContext);
export const useSetProjectState = () => useContext(ProjectStateUpdateContext);

// Provider Component
export const ProjectStateProvider = ({ children }) => {
    const [projectState, setProjectState] = useState({ mode: 'create' }); // Default mode

    return (
        <ProjectStateContext.Provider value={projectState}>
            <ProjectStateUpdateContext.Provider value={setProjectState}>
                {children}
            </ProjectStateUpdateContext.Provider>
        </ProjectStateContext.Provider>
    );
};
