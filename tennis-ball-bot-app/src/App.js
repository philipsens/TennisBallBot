import React, {useEffect, useState} from 'react';
import './App.css';
import Header from "./components/Header";
import Button from "./components/Button";
import ZoneSelector from "./components/ZoneSelector";
import {CollectionMode} from "./CollectionMode";

const baseURI = process.env.REACT_APP_API_URL;
const collectionModeURI = baseURI + 'collectionMode';

function App() {
    const [collectionMode, setCollectionMode] = useState(CollectionMode.ZONE)

    useEffect(() => {
        fetch( collectionModeURI)
            .then(response => response.json())
            .then(data => setCollectionMode(data[0].collectionMode))
    }, [])

    return (
        <div className="App">
            <Header/>
            <main>
                <div className="button-wrapper">
                    <Button onClick={() => setCollectionMode(CollectionMode.DISABLED)} primary>Return to the collection
                        area</Button>
                    <Button onClick={() => setCollectionMode(CollectionMode.ZONE)} accent>Collect selected zones</Button>
                    <Button onClick={() => setCollectionMode(CollectionMode.ALL)} secondary>Collect everywhere</Button>
                </div>
                <ZoneSelector collectionMode={collectionMode}/>
            </main>
        </div>
    );
}

export default App;
