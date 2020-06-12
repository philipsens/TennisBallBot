import React, {useEffect, useState} from 'react'
import Zone from "./Zone";
import {CollectionMode} from "../CollectionMode";

const baseURI = process.env.REACT_APP_API_URL;
const collectionURI = baseURI + 'collection';
const zoneURI = baseURI + 'zone';

export default function ZoneSelector({collectionMode}) {
    const [selectedCollection, setSelectedCollection] = useState(0);
    const [selectedZone, setSelectedZone] = useState(-1);
    const zones = [...new Array(12)].map((_, i) => ({
        middle: i === 4 || i === 7,
        corner: i === 0 || i === 2 || i === 9 || i === 11,
        disabled: collectionMode === CollectionMode.DISABLED
    }));

    useEffect(() => {
        fetch(collectionURI)
            .then(response => response.json())
            .then(data => setSelectedCollection(data[0].id))

        fetch(zoneURI)
            .then(response => response.json())
            .then(data => setSelectedZone(data[0].id))
    }, [])

    useEffect(() => {
        fetch(collectionURI, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: selectedCollection})
        })
            .catch(error => console.log(error))
    }, [selectedCollection])

    useEffect(() => {
        fetch(zoneURI, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: setSelectedZone})
        })
            .catch(error => console.log(error))
    }, [selectedZone])

    return (
        <div className="zone-selector">
            {zones.map((zone, i) => (
                <Zone
                    key={i}
                    onCollectionSelected={() => setSelectedCollection(i)}
                    onZoneSelected={() => setSelectedZone(i)}
                    selected={i === selectedZone || collectionMode === CollectionMode.ALL}
                    collection={i === selectedCollection}
                    {...zone}
                />
            ))}
        </div>
    );
}
