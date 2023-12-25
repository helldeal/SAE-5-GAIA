import { useIsFocused } from "@react-navigation/native";
import React, { useEffect, useRef, useState } from "react";
import { View, Text, Button, Image, TouchableOpacity, Linking, Pressable } from "react-native";
import MapView, { MapType, Marker } from "react-native-maps";
import * as Location from "expo-location";
import { SafeAreaView } from "react-native-safe-area-context";
import { getAllPoints, getPointsbyRegion } from "../../dao/MapPoint";
import ModalComponent from "../component/Modal";
import { styles } from "../../style/style";
import MapModalComponent from "../component/MapModal";

export default function Map() {
  const initialRegion={
    latitude: 47.200819319828305,
    latitudeDelta: 0.2705200915647197,
    longitude: -1.5608386136591434,
    longitudeDelta: 0.18985044211149216,
  }
  const standardMapType=[
  {
    "featureType": "poi",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  }
]
  const isFocused = useIsFocused();
  const [currentLocation, setCurrentLocation] = useState(null);
  const [region, setRegion] = useState(initialRegion);
  const [points, setPoints] = useState(getPointsbyRegion(region));
  const [mapType, setMapType] = useState<MapType>('standard');
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedPoint, setSelectedpoint] = useState(null);
  
  const markerIcons = {
    Pharmacie: require("./../../assets/map-icons/pharma.png"),
    Centre: require("./../../assets/map-icons/hopital.png"),
    Etablissement: require("./../../assets/map-icons/clinique.png"),
    Maison: require("./../../assets/map-icons/maison_de_sante.png"),
    satelite: require("./../../assets/map-icons/satelite.png"),
    map: require("./../../assets/map-icons/map.png")
  }
  const colorOf = {
    Pharmacie: "25, 170, 147",
    Centre: "254, 135, 88",
    Etablissement: "1, 94, 210",
    Maison: "0, 236, 156",
  };
  const [satelliteButtonIcon, setSatelliteButtonIcon] = useState(markerIcons.satelite);

  const toggleMapType = () => {
    // Toggle between 'standard' and 'satellite' view modes
    if (mapType === 'standard') {
      setMapType('satellite');
      setSatelliteButtonIcon(markerIcons.map); // Change button icon to 'map.png'
    } else {
      setMapType('standard');
      setSatelliteButtonIcon(markerIcons.satelite); // Change button icon back to 'satelite.png'
    }
  };

  const openModal = (point: any) => {
    setIsModalVisible(true);
    setSelectedpoint(point);
  };
  const closeModal = () => {
    setIsModalVisible(false);
  };
  const contact = () => {
    if(selectedPoint.phone) {
      Linking.openURL(`tel:${selectedPoint.phone}`);
    } else {
      console.log("No phone number");
    }
  };
  const modalContent = selectedPoint ? (
    <View>
      <Text numberOfLines={2} ellipsizeMode="tail" style={styles.modalTitle}>{selectedPoint.Name}</Text>
      <Text style={styles.modalType}>{selectedPoint.type}</Text>
      <Text>{selectedPoint.adress}</Text>
      {selectedPoint.phone != null ? (
        <Button title="Contacter" onPress={contact}/>
      ): <Text>No phone number available here... 🙁</Text>}
    </View>
  ) : null;
  

  useEffect(() => {
    if (isFocused) {
      console.log("Nav on Map Page");
      const getLocation = async () => {
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== "granted") {
          console.log("Permission to access location was denied");
          return;
        }
        let location = await Location.getCurrentPositionAsync({});
        setCurrentLocation(location.coords);
        const animateToCoordinat = (lat, long) => {
          this.map.animateCamera({
            center: {
              latitude: lat,
              longitude: long,
            },
            duration: 1000,
          });
        };
        animateToCoordinat(location.coords.latitude, location.coords.longitude);
      };

      getLocation();
    }
  }, [isFocused]);

  useEffect(() => {
    const newPoints = getPointsbyRegion(region);
    setPoints(newPoints);
  }, [region]);

  return (
    <View>
      <MapView
        ref={(map) => (this.map = map)}
        style={{ width: "100%", height: "100%" }}
        initialRegion={initialRegion}
        onRegionChangeComplete={(region, gesture) => (gesture.isGesture)? setRegion(region):null}
        customMapStyle={standardMapType}
        toolbarEnabled={false}
        //showsUserLocation={currentLocation}
      >
        {points &&

          points.map((point) => {

            const getIcon = markerIcons[point.type.split(' ')[0]]
                return (
                  <Marker
                    key={point.id}
                    coordinate={{
                      latitude: point.latitude,
                      longitude: point.longitude,
                    }}
                    title={point.Name}
                    onPress={() => openModal(point)}
                  >
                    <Image source={getIcon} style={{ width: 25, height: 25 }} />
                  </Marker>
                );
          })}
      </MapView>
      <TouchableOpacity style={{ position: 'absolute', top: 20, right: 20 }}>
        <View style={{ backgroundColor: 'white', padding: 10, borderRadius: 5 }}>
          <Image source={satelliteButtonIcon}  style={{ width: 40, height: 40 }} />
        </View>
      </TouchableOpacity>
      <MapModalComponent 
        visible={isModalVisible} 
        onClose={closeModal} 
        children={modalContent} 
        icon={markerIcons[selectedPoint?.type.split(' ')[0]]} 
        color={colorOf[selectedPoint?.type.split(' ')[0]]}
      />
    </View>
  );
}
function setMapType(arg0: string) {
  throw new Error("Function not implemented.");
}
