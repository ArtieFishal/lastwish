import React from 'react';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import CreateGuidePage from './pages/CreateGuidePage';
import PricingPage from './pages/PricingPage';
import FaqPage from './pages/FaqPage';
import DownloadPage from './pages/DownloadPage';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout><HomePage /></Layout>,
  },
  {
    path: "/create",
    element: <Layout><CreateGuidePage /></Layout>,
  },
  {
    path: "/pricing",
    element: <Layout><PricingPage /></Layout>,
  },
  {
    path: "/faq",
    element: <Layout><FaqPage /></Layout>,
  },
  {
    path: "/download",
    element: <Layout><DownloadPage /></Layout>,
  },
]);

function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
