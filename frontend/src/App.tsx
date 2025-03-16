import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Provider } from 'react-redux';
import { theme } from './styles/theme';
import { store } from './store';
import MainLayout from './components/layout/MainLayout';
import ErrorBoundary from './components/feedback/ErrorBoundary';
import { ToastProvider } from './components/feedback/Toast';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';

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
                <Routes>
                  <Route
                    path="/"
                    element={
                      <MainLayout>
                        <Dashboard />
                      </MainLayout>
                    }
                  />
                  <Route 
                    path="/clients" 
                    element={
                      <MainLayout title="Clients">
                        <div>Clients-Seite</div>
                      </MainLayout>
                    } 
                  />
                  <Route 
                    path="/server" 
                    element={
                      <MainLayout title="Server">
                        <div>Server-Seite</div>
                      </MainLayout>
                    } 
                  />
                  <Route 
                    path="/settings" 
                    element={
                      <MainLayout title="Einstellungen">
                        <div>Einstellungen-Seite</div>
                      </MainLayout>
                    } 
                  />
                  <Route path="*" element={<NotFound />} />
                </Routes>
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