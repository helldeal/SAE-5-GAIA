import { useIsFocused } from "@react-navigation/native";
import React, { useEffect, useRef, useState } from "react";
import { View, Text, FlatList, TouchableOpacity, Image } from "react-native";
import { searchMed } from "../../dao/Search";
import { styles } from "../../style/style";
import { Icon, Input } from "react-native-elements";
import MedIconByType from "../component/MedIconByType";
import { Navigation } from "react-native-feather";
import { SafeAreaView } from "react-native-safe-area-context";
import { getUserByID } from "../../dao/Storage";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { getPAfromMed } from "../../dao/Meds";

export default function Search({ route, navigation }) {
  const textInputRef = React.useRef(null);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (textInputRef.current) {
      setTimeout(() => textInputRef.current.focus(), 200);
    }
  }, []);
  const [search, setSearch] = useState([]);
  const isFocused = useIsFocused();
  const init = async () => {
    const currentId = await AsyncStorage.getItem("currentUser");
    const current = await getUserByID(JSON.parse(currentId));
    setUser(current);
  };
  useEffect(() => {
    if (isFocused) {
      console.log("Nav on Search Page");
      init();
    }
  }, [isFocused]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.searchBarwQR} className="mt-3 px-4">
        <View style={styles.searchBar}>
          <Input
            style={styles.searchBarInput}
            ref={textInputRef}
            placeholder="Doliprane, Aspirine ..."
            placeholderTextColor="#9CDE00"
            leftIcon={
              <Icon
                name="arrow-left" // Change to your icon's name
                type="feather"
                size={24}
                color="#9CDE00"
                onPress={() => {
                  navigation.goBack();
                }}
              />
            }
            rightIcon={{ type: "feathers", name: "search", color: "#9CDE00" }}
            inputContainerStyle={styles.searchBarContainer}
            onChangeText={(text) => {
              const newSearch = searchMed(text);
              if (newSearch.length > 0) {
                setSearch(newSearch);
              } else {
                setSearch(searchMed("E"));
              }
            }}
          />
        </View>
      </View>
      <FlatList
        data={search}
        keyExtractor={(_item, index) => index.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.listItem}
            className="flex justify-start align-middle"
            onPress={() => navigation.navigate("Drug", { drugCIS: item.CIS })}
          >
            <MedIconByType type={item.type} />
            <View className="ml-4 flex-1 flex-row justify-between items-center">
              <Text className="flex-1">{item.Name}</Text>
              {user.preference
                .map((allergie) =>
                  Array.from(getPAfromMed(item.CIS)).includes(allergie)
                )
                .some((bool) => bool) && (
                <View className=" items-center">
                  <Image
                    className={"h-5 w-5 ml-1"}
                    source={require("../../assets/allergy.png")}
                  />
                  <Text className="ml-2 text-red-500 font-bold">Allergie</Text>
                </View>
              )}
            </View>
          </TouchableOpacity>
        )}
      />
    </SafeAreaView>
  );
}
