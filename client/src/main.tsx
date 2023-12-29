import * as ReactDOM from 'react-dom/client'
import { ThemeProvider } from '@emotion/react'
import { CssBaseline } from '@mui/material'
import theme from './theme'
import App from './App'
import { BrowserRouter } from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <BrowserRouter>
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <App />
        </ThemeProvider>
    </BrowserRouter>
)
