import React, {useState} from 'react';
import './App.css';
import Header from "./components/Header";
import Button from "./components/Button";
import ZoneSelector from "./components/ZoneSelector";

function App() {
    const [collectionMode, setCollecionMode] = useState(-1)

    return (
        <div className="App">
            <Header/>
            <main>
                <div className="button-wrapper">
                    <Button onClick={() => setCollecionMode('disabled')} primary>Return to the collection area</Button>
                    <Button onClick={() => setCollecionMode(-1)} accent>Collect selected zones</Button>
                    <Button onClick={() => setCollecionMode('all')} secondary>Collect everywhere</Button>
                </div>
                <ZoneSelector collectionMode={collectionMode} />
            </main>
        </div>
    );
}

export default App;
