import React, { useEffect, useState } from "react";
import {
  View,
  StyleSheet,
  Text,
  StatusBar,
  TextInput,
  Button,
  TouchableOpacity
} from "react-native";
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Link, NavigationProp, ParamListBase } from "@react-navigation/native";
import { useIsFocused } from "@react-navigation/native";
import * as ImagePicker from 'expo-image-picker';
import callGoogleVisionAsync from "../../ocr/helperFunctions";
import { styles } from "../../style/style";

interface IHomeProps {
  navigation: NavigationProp<ParamListBase>;
}
export default function Home({ navigation }: IHomeProps) {
  const isFocused = useIsFocused();

  const [user, setUser] = useState<User | null>(null);
  const [search, setSearch] = useState("");

  const eventHandler = async () => {
      //const isTutoComplete = await AsyncStorage.getItem("tutoComplete");
      const isConnected = await AsyncStorage.getItem("users");
      if (isConnected === null) {
        // L'utilisateur se connecte pour la première fois
        navigation.navigate("CreateProfile");
        
      } /*else if(isTutoComplete === null){
        alert("Va falloir faire le tuto bro");
  
      }*/else{
        setUser(JSON.parse(isConnected));
        console.log("user :",isConnected)
      }
  };

  const updateSearch = (text: string) => {
    setSearch(text);
  };
  
  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      base64: true, //return base64 data.
      //this will allow the Vision API to read this image.
    });
    if (!result.canceled) { //if the user submits an image,
      //setImage(result.assets[0].uri);
      //run the onSubmit handler and pass in the image data. 
      const googleText = await callGoogleVisionAsync(result.assets[0].base64);
      console.log("OCR :",googleText.text)
      alert(googleText.text)
    }
  };

 
  useEffect(() => {
    if(isFocused){ 
      console.log("Nav on Home Page")
      eventHandler();
    }
  },[isFocused]); 
  

  return (
    <View style={styles.container}> 
      <View style={styles.header}>
        <Text style={styles.subtitle}>Welcome back</Text>
        <Text style={styles.title}>Alexandre</Text>
      </View>
      <View style={styles.searchContainer}>
        <Text style={styles.title2}>Recherche d’un médicament</Text>
        <View style={styles.searchBarwQR}>  
          <View style={styles.searchBar}>
            <TextInput
              style={styles.searchBarInput}
              placeholder="Doliprane, Aspirine ..."
              onChangeText={updateSearch}
              value={search}
            />
          </View>
          <TouchableOpacity  onPress={pickImage} style={styles.searchQR}>
            {/* <Image
              source={{ uri: "App/assets/images/Scan. png" }}
            /> */}
          </TouchableOpacity>
        </View>
      </View>
      <View style={styles.traitementContainer}>
        <Text style={styles.title2}>Suivis d'un traitement</Text>
      </View>
    </View>
  );
}


