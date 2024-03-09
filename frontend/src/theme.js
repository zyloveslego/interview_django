import { createTheme } from '@mui/material/';

export const theme = createTheme({
    palette: {
        primary: {
            main: "#7E5F50",
            light: "#A07764",
            dark: "#5E473C"
        },

        text: {
            primary: "#3f302a"
        }
    }

})

console.log(theme);