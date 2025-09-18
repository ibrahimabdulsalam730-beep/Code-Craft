import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AOS from 'aos';
import 'aos/dist/aos.css';
import Home from './Home.jsx';
import Python1 from "./Python.jsx";
import HTML from "./HTML.jsx";
import CSS from "./CSS.jsx";
import JavaScript from './Javascript.jsx';
import MYSQL from './MYSQL.jsx';
import Contact from './Contact.jsx';
import About from './About.jsx';

function App() {
    useEffect(() => {
        // Global AOS initialization
        AOS.init({
            duration: 1000,
            once: true,
            mirror: false,
        });
    }, []);

    return (
        <Router>
            <Routes>
                {/* Public routes */}
                <Route path="/" element={<Home />} />
                <Route path="/home" element={<Home />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/about" element={<About />} />
                <Route path="/python1" element={<Python1 />} />
                <Route path="/html" element={<HTML />} />
                <Route path="/css" element={<CSS />} />
                <Route path="/javascript" element={<JavaScript />} />
                <Route path="/mysql" element={<MYSQL />} />
            </Routes>
        </Router>
    );
}

export default App;