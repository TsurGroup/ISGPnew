// src/components/app-bar/CustomAppBar.jsx
import React from "react";
import { AppBar, Toolbar, Typography, Box, Button } from "@mui/material";
import ScienceIcon from "@mui/icons-material/Science";
import HomeIcon from "@mui/icons-material/Home";

const CustomAppBar = ({ version }) => {
  // Function to clear the specific cookie 'projectName'
  const clearProjectNameCookie = () => {
    // Remove the projectName cookie by setting its expiration to the past
    document.cookie = "projectName=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + window.location.hostname;
    document.cookie = "projectName=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
  };

  // Home button click handler
  const handleHomeClick = () => {
    clearProjectNameCookie();  // Clear the projectName cookie
    window.location.href = "/";  // Navigate to home
  };

  return (
    <AppBar
      position="sticky"
      color="primary"
      elevation={0}
      sx={{ bgcolor: "background.paper" }}
    >
      <Toolbar
        variant="dense"
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          minHeight: { xs: "32px", sm: "40px" },
          padding: { xs: "0 4px", sm: "0 8px" },
        }}
      >
        {/* Home Button (No text, larger icon, no hover effect) */}
        <Button
          onClick={handleHomeClick}
          sx={{
            position: "absolute",
            left: "8px",
            color: "text.primary",  // Ensure button is visible
            minWidth: 0,  // Remove button text
            padding: 0,  // Remove padding
            "&:hover": {
              backgroundColor: "transparent",  // No hover effect
            },
          }}
        >
          <HomeIcon sx={{ fontSize: "2rem" }} /> {/* Directly applying larger size */}
        </Button>

        {/* Title: ISGP² */}
        <Box
          sx={{
            position: "absolute",
            left: "50%",
            transform: "translateX(-50%)",
            display: "flex",
            alignItems: "center",
          }}
        >
          <Typography
            variant="h2"
            component="p"
            color="textPrimary"
            sx={{ marginRight: "4px" }}
          >
            ISGP
            <Typography
              component="span"
              variant="caption"
              sx={{ verticalAlign: "super", fontSize: "0.6em" }}
            >
              2
            </Typography>
          </Typography>
          <ScienceIcon sx={{ color: "primary.main" }} />
        </Box>

        {/* Version Display (Moved to the right) */}
        <Typography
          variant="h3"
          color="textPrimary"
          sx={{
            padding: "5px",
            position: "absolute",
            right: "8px",
            fontWeight: 400,  // Less bold
          }}
        >
          {version}
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default CustomAppBar;
