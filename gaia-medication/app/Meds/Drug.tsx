import { useIsFocused } from "@react-navigation/native";
import React, { useEffect, useState } from "react";
import { View, Text, FlatList, TouchableOpacity, Modal, Pressable,StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { getMedbyCIS } from "../../dao/Meds";
import { addItemToList, getUserByID, readList, removeItemFromStock } from "../../dao/Storage";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Loading from "../component/Loading";
import { Button, Input } from "react-native-elements";
import { styles } from "../../style/style";
import DrugModal from "../component/Modal";
import ModalComponent from "../component/Modal";

export default function Drug({ route }) {
  const [drugModalVisible, setDrugModalVisible] = useState(false);
  const [drugsToAdd, setDrugsToAdd] = useState(null);
  const isFocused = useIsFocused();
  const [user, setUser] = useState<User | null>(null);
  const [stock, setStock] = useState(null);

  const { drugCIS } = route.params;
  const drug = getMedbyCIS(drugCIS);

  const init = async () => {
    const currentId = await AsyncStorage.getItem("currentUser");
    const current = await getUserByID(JSON.parse(currentId));
    setUser(current);
    const stockList = await readList("stock");
    setStock(
      stockList.filter(
        (item) => item.idUser == currentId && item.CIS == drugCIS
      )
    );
  };

  useEffect(() => {
    if (isFocused) {
      console.log("Nav on Drug Page :", drug.CIS);
      init();
    }
  }, [isFocused]);

  const addToStock = async (item) => {
    try {
      const addstock: Stock = {
        idUser: user.id,
        CIP: item.CIP,
        CIS: item.CIS,
        qte: 0,
      };
      console.log(addstock);

      await addItemToList("stock", addstock);
      setStock([...stock, addstock]);
    } catch (e) {
      console.log(e);
    }
  };
  
  const deleteFromStock = async (cis, cip, idUser) => {
    try {
      await removeItemFromStock(cis, cip, idUser);
      init()
    } catch (e) {
      console.log(e);
    }
  };
  return (
    <View style={styles.container}>
      {drug && stock && user && (
        <>
          <Text>Name : {drug.Name}</Text>
          <Text>Administration : {drug.Administration_way}</Text>
          <Text>Type : {drug.Shape}</Text>
          <Text>Commerce : {drug.Marketed}</Text>
          <FlatList
            data={drug.Values}
            keyExtractor={(item, index) => index.toString()}
            renderItem={({ item }) => {
              const alreadyStocked =
                stock.find((stock) => stock.CIP === item.CIP) != null;
              return (
                <>
                  <Text>Produit :</Text>
                  <Text>CIP : {item.CIP}</Text>
                  <Text>Description : {item.Denomination}</Text>
                  {drug.Marketed == "Commercialisée" &&
                    (item.Price_with_taxes ? (
                      <>
                        <Text>Prix : {item.Price_with_taxes}€</Text>
                        <Text>Remboursement : {item.Remboursement}</Text>
                      </>
                    ) : (
                      <>
                        <Text>Prix : Prix libre</Text>
                        <Text>Remboursement : Non remboursable</Text>
                      </>
                    ))}

                  {alreadyStocked ? (
                    <><TouchableOpacity className=" bg-green-400 text-center">
                      <Text className="text-center">In stock</Text>
                    </TouchableOpacity>
                    <TouchableOpacity className=" bg-red-400 text-center"
                      onPress={() => deleteFromStock(item.CIS, item.CIP, user.id)}
                    >
                        <Text className="text-center">❌</Text>
                      </TouchableOpacity></>
                  ) : (
                    <TouchableOpacity className=" bg-blue-400" onPress={() => {
                      setDrugsToAdd(item)
                      setDrugModalVisible(true)
                    }}>
                      <Text className="text-center">Add</Text>
                    </TouchableOpacity>
                  )}
                </>
              );
            }}
          />
          <ModalComponent visible={drugModalVisible} onClose={()=>setDrugModalVisible(!drugModalVisible)}>
            <Text>Ajouter un Medicament</Text>
            <TouchableOpacity className=" bg-blue-400" onPress={() => {
              addToStock(drugsToAdd)
              setDrugModalVisible(!drugModalVisible)
            }}>
              <Text className="text-center">Add</Text>
            </TouchableOpacity>
          </ModalComponent>
        </>
      )}
      {(!drug || !stock || !user) && <Loading />}
    </View>
  );
}

