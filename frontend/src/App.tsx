import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Provider } from 'react-redux';
import { theme } from './styles/theme';
import { store } from './store';
import ErrorBoundary from './components/feedback/ErrorBoundary';
import { ToastProvider } from './components/feedback/Toast';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
import { Box } from '@mui/material';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 Minuten
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <ToastProvider>
            <ErrorBoundary>
              <Router>
                <Box sx={{ 
                  minHeight: '100vh', 
                  backgroundColor: '#f5f7fa', 
                  p: { xs: 2, sm: 3 },
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'flex-start'
                }}>
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="*" element={<NotFound />} />
                  </Routes>
                </Box>
              </Router>
            </ErrorBoundary>
          </ToastProvider>
        </ThemeProvider>
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </Provider>
  );
}

export default App; 