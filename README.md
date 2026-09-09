# skill-setu-backend

## Initial Setup (One-Time)

### Prerequisites
* **Python:** `3.11.9` (Install before proceeding)
* **Django:** `5.2 LTS`

---

### 1. Clone the Repository
```bash
git clone [https://github.com/Pranav-Kukreja10/skill-setu-backend](https://github.com/Pranav-Kukreja10/skill-setu-backend)
cd skillsetu-backend
```

---

### 2. Create and Activate Virtual Environment

**Windows:**
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

---

### 3. Verify Virtual Environment
Confirm that the virtual environment is running Python 3.11.9:
```bash
python -c "import sys; print(sys.version)"
```

---

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 5. Initialize Database
Apply migrations to configure the local SQLite database:
```bash
python manage.py migrate
```

---

(Do this step everytime to run backend Server)
### 6. Start the Development Server
```bash
python manage.py runserver
```

---

### 7. Access API Documentation
Once the server is running, open the interactive Swagger UI in your browser:
* **Interactive Docs:** [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)
* **OpenAPI Schema:** [http://127.0.0.1:8000/api/v1/openapi.json](http://127.0.0.1:8000/api/v1/openapi.json)

Do the following to connect frontend and backend for testing:
# skill-setu-frontend 

## Initial Setup & Backend Connection

This guide walks you through setting up the React (Vite) frontend repository and wiring it up to consume the live Django Ninja API contract.

---

### 1. Initialize the Vite Project
Run the following commands in your workspace root:
```bash
npm create vite@latest skillsetu-frontend -- --template react
cd skillsetu-frontend
npm install
```

---

### 2. Install Network & State Libraries
Install Axios and TanStack React Query for data fetching and caching:
```bash
npm install axios @tanstack/react-query
```

---

### 3. Configure Environment Variables
Create a `.env` file in the root of `skillsetu-frontend`:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

> **Note:** Never hardcode the backend URL inside your components. Always consume `import.meta.env.VITE_API_BASE_URL`.

---

### 4. Setup Central Axios Client
Create `src/lib/api.js` to establish the base API instance:
```javascript
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

---

### 5. Wrap the App with QueryClientProvider
Update `src/main.jsx` to enable React Query across your entire application:
```jsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App.jsx';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);

```

---

### 6. Verify Full Connection (Smoke Test)
Replace the contents of `src/App.jsx` with this smoke-test component to verify real-time communication with the backend stubs:
```jsx
import { useQuery } from '@tanstack/react-query';
import { api } from './lib/api';

const fetchStudents = async () => {
  const { data } = await api.get('/students/');
  return data;
};

export default function App() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['students'],
    queryFn: fetchStudents,
  });

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Skill Setu - Integration Test</h1>
      {isLoading && <p>Connecting to backend API...</p>}
      {isError && (
        <p style={{ color: 'red' }}>
          Connection failed: {error.message}. Ensure the Django backend is running at [http://127.0.0.1:8000](http://127.0.0.1:8000).
        </p>
      )}
      {data && (
        <div>
          <p style={{ color: 'green', fontWeight: 'bold' }}>✓ Successfully connected to Django Ninja API!</p>
          <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: '6px' }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}
```

---

### 7. Run the Frontend Server
```bash
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser. With the Django backend running on port `8000`, you should see the raw student stub JSON displayed directly on the page.

---

### 8. API Contract Reference
Refer to the Swagger documentation for available routes, request bodies, and response structures:
* **Interactive Contract Docs:**  http://127.0.0.1:8000/api/v1/docs

*Note Frontend and backend must run together to Show the following output: 

<img width="1919" height="987" alt="image" src="https://github.com/user-attachments/assets/5d0a653d-de0e-4bc7-9bf1-f2ab4894e0d4" />


