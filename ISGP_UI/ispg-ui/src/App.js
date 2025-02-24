import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import { Box } from "@mui/material";

import CustomAppBar from "./components/global/AppBar.jsx";
import Home from "./components/home/Home.jsx";
import ExperimentData from "./components/data-form/ExperimentData.jsx";
import AlgorithmParameters from "./components/experiment-data/AlgorithmParameters.jsx";
import DataDashboard from "./components/data-dashboard/DataDashboard.jsx";
import LoadedDataDashboard from "./components/data-dashboard/load-data-dashboard/LoadedDataDashboard.jsx";
import CompletionScreen from "./components/completion-screen/CompletionScreen.jsx";
import PageNotFound from "./components/page-not-found/PageNotFound.jsx";

import { ProjectStateProvider } from "./contexts/ProjectStateContext"; // Adjust the path

function App() {
  const [version, setVersion] = useState("");

  return (
    <ProjectStateProvider>
      <Box>
        <CustomAppBar version={version} />

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home setVersion={setVersion} />} />
          <Route path="/Data" element={<ExperimentData />} />
          <Route path="/AlgorithmParameters" element={<AlgorithmParameters />} />
          <Route path="/DataDashboard" element={<DataDashboard />} />
          <Route path="/CompletionScreen" element={<CompletionScreen />} />
          <Route path="/LoadedDataDashboard" element={<LoadedDataDashboard />} />
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </Box>
    </ProjectStateProvider>
  );
}

export default App;
