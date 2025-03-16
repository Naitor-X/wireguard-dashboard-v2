# Frontend-Komponenten

Dieses Verzeichnis enthält alle wiederverwendbaren React-Komponenten für das WireGuard Dashboard.

## Struktur

- **layout/** - Layout-Komponenten für die Anwendungsstruktur
  - `MainLayout.tsx` - Hauptlayout mit Navigation und Header
  - `ProtectedRoute.tsx` - Schützt Routen vor unauthentifizierten Zugriffen

- **feedback/** - Komponenten für Feedback und Benachrichtigungen
  - `ErrorBoundary.tsx` - Fängt Fehler in der Komponenten-Hierarchie ab
  - `ErrorDisplay.tsx` - Zeigt Fehlermeldungen an
  - `LoadingState.tsx` - Zeigt Ladezustände an
  - `Toast.tsx` - Toast-Benachrichtigungssystem

- **ui/** - Grundlegende UI-Komponenten
  - `Button.tsx` - Erweiterte Button-Komponente
  - `Input.tsx` - Erweiterte Input-Komponente
  - `Card.tsx` - Erweiterte Card-Komponente

## Verwendung

### Layout-Komponenten

```tsx
import { MainLayout, ProtectedRoute } from './components/layout';

// Geschützte Route mit Layout
<ProtectedRoute>
  <MainLayout title="Dashboard">
    <YourComponent />
  </MainLayout>
</ProtectedRoute>
```

### Feedback-Komponenten

```tsx
import { ErrorDisplay, LoadingState, useToast } from './components/feedback';

// In deiner Komponente
const { showToast } = useToast();

// Zeige einen Ladeindikator
<LoadingState message="Daten werden geladen..." />

// Zeige einen Fehler an
<ErrorDisplay 
  title="Fehler beim Laden" 
  message="Die Daten konnten nicht geladen werden."
  onRetry={() => fetchData()} 
/>

// Zeige eine Toast-Benachrichtigung
showToast({
  message: "Erfolgreich gespeichert",
  type: "success"
});
```

### UI-Komponenten

```tsx
import { Button, Input, Card } from './components/ui';

// Button mit Ladeindikator
<Button 
  isLoading={isSubmitting}
  loadingText="Wird gespeichert..."
  onClick={handleSubmit}
>
  Speichern
</Button>

// Input mit Icon
<Input
  label="Benutzername"
  startIcon={<PersonIcon />}
  placeholder="Geben Sie Ihren Benutzernamen ein"
/>

// Card mit Titel und Footer
<Card
  title="Benutzerdetails"
  subtitle="Persönliche Informationen"
  footer={<Button>Bearbeiten</Button>}
  dividers
>
  <p>Inhalt der Karte</p>
</Card>
``` 