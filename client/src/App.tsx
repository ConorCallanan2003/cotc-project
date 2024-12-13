import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import React from "react";
import Homepage from "./pages/Home.tsx";
import Graph from "./pages/Graph.tsx";
import Layout from "./Layout.tsx";
import MetricPage from "./pages/Graph.tsx";

function App() {
  return (
    <div className="h-screen w-screen flex justify-center items-center">
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route index element={<Homepage />} />
            <Route path="/metric/:id" element={<MetricPage />} />
            {/* <Route path="/contact" element={<Contact />} /> */}
            {/* <Route path="/*" element={<NoPage />} /> */}
          </Routes>
        </Layout>
      </BrowserRouter>
    </div>
  );
}

export default App;
