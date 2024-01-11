import React, { useEffect, useState } from "react";
import RNPickerSelect from "react-native-picker-select";
import {
  FlatList,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { Input } from "react-native-elements";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { NavigationProp, ParamListBase } from "@react-navigation/native";
import { SafeAreaView } from "react-native-safe-area-context";
import { UserIdAutoIncrement, addItemToList } from "../../dao/Storage";
import { SearchAllergy } from "../../dao/Search";
import { styles } from "../../style/style";
import CustomButton from "../component/CustomButton";
import AllergySelector from "../component/AllergySelector";
import TutorialBubble from "../component/TutorialBubble";
import DateTimePicker from "@react-native-community/datetimepicker";
import { ArrowLeft } from "react-native-feather";
import GoBackButton from "../component/GoBackButton";

interface ICreateProps {
  navigation: NavigationProp<ParamListBase>;
}

export default function CreateProfile({ navigation }: ICreateProps) {
  const [lastname, setLastname] = useState("");
  const [firstname, setFirstname] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState<Date | null>(null);
  const [weight, setWeight] = useState<number>();
  const [gender, setGender] = useState("");
  const [preference, setPreference] = useState([]);
  const [showDatePicker, setShowDatePicker] = useState(false);

  const [isValidFirstname, setIsValidFirstname] = useState(true);
  const [isValidLastname, setIsValidLastname] = useState(true);
  const [isValidWeight, setIsValidWeight] = useState(true);

  const [validFirstPart, setValidFirstPart] = useState(false);
  const [isAllergySelectorValid, setIsAllergySelectorValid] = useState(false);

  const [firstConnection, setFirstConnection] = useState("");
  const [tutoStep, setTutoStep] = useState(0);
  const [TutoCreate, setTutoCreate] = useState("0");

  const isFirstFormEmpty = !firstname || !lastname || !gender;

  const isFormEmpty =
    !firstname ||
    !lastname ||
    !gender ||
    !dateOfBirth ||
    !weight ||
    !isValidWeight;

  const validateFirstname = () => {
    setIsValidFirstname(firstname.length >= 2);
  };

  const validateLastname = () => {
    setIsValidLastname(lastname.length >= 2);
  };

  const validateWeight = () => {
    if (weight > 0 || weight <= 999) {
      setIsValidWeight(true);
    } else {
      setIsValidWeight(false);
    }
  };

  const handleAllergySelectorValidation = (isValid) => {
    setIsAllergySelectorValid(isValid);
  };

  function formatDateToDDMMYYYY(date: Date) {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const formattedDay = day < 10 ? `0${day}` : day;
    const formattedMonth = month < 10 ? `0${month}` : month;
    const formattedDate = `${formattedDay}/${formattedMonth}/${year}`;

    return formattedDate;
  }

  const init = async () => {
    setFirstConnection(await AsyncStorage.getItem("isFirstConnection"));
    setTutoCreate(await AsyncStorage.getItem("TutoCreate"));
  };

  useEffect(() => {
    console.log("Nav on CreationProfile Page");
    init();
  }, []);

  const handleTuto = (isClicked, step) => {
    if (isClicked) {
      if (step === 2) {
        setTutoStep(2);
      } else if (tutoStep < 1) {
        setTutoStep(tutoStep + 1);
      }
    }
  };

  const handleFirstSumbit = () => {
    if (validFirstPart) {
      setValidFirstPart(false);
    } else {
      if (!isValidFirstname || !isValidLastname || isFirstFormEmpty) {
        console.log(`error not valid`);
      } else {
        setValidFirstPart(true);
        handleTuto(true, 2);
      }
    }
  };

  const handleSumbit = async () => {
    if (!isValidFirstname || !isValidLastname || isFormEmpty) {
      console.log(`error not valid`);
    } else {
      try {
        if (firstConnection === "true") {
          await AsyncStorage.setItem("isFirstConnection", "false");
          await AsyncStorage.setItem("TutoCreate", "1");
        }
        const user: User = {
          id: await UserIdAutoIncrement(),
          firstname,
          lastname,
          dateOfBirth,
          weight,
          gender,
          preference,
        };
        console.log(user);

        await addItemToList("users", user);
        await AsyncStorage.setItem("currentUser", JSON.stringify(user.id));
        navigation.navigate("Home");
      } catch (e) {
        console.log(e);
      }
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {tutoStep === 0 && TutoCreate === "0" && (
        <TutorialBubble
          isClicked={handleTuto}
          styleAdded={{ top: "60%", left: "5%" }}
          text={
            "Bienvenue sur Gaïa,\nmais avant tout, permettez-nous\nde créer votre profil. 1/2"
          }
        ></TutorialBubble>
      )}
      {tutoStep === 1 && TutoCreate === "0" && (
        <TutorialBubble
          isClicked={handleTuto}
          styleAdded={{ top: "60%", left: "5%" }}
          text={"Veuillez renseigner\nles différents champs. 2/2"}
        ></TutorialBubble>
      )}
      {tutoStep === 2 && TutoCreate === "0" && (
        <TutorialBubble
          isClicked={handleTuto}
          styleAdded={{ top: "60%", left: "3%" }}
          text={"Veuillez renseigner ces autres champs. 1/1"}
        ></TutorialBubble>
      )}

      <GoBackButton navigation={navigation}></GoBackButton>

      <Text className=" text-center my-6 text-2xl text-neutral-700 font-bold">
        Création de profil
      </Text>
      {!validFirstPart && (
        <>
          <Input
            label="Prénom"
            labelStyle={styles.label}
            placeholder="Entrez votre prénom"
            placeholderTextColor={"#dedede"}
            onChangeText={(text) =>
              setFirstname(text.charAt(0).toUpperCase() + text.slice(1))
            }
            onBlur={validateFirstname}
            value={firstname}
            renderErrorMessage={isValidFirstname}
          />
          {!isValidFirstname && (
            <Text style={stylesProfile.errorText}>
              Le prénom doit comporter au moins 1 caractères.
            </Text>
          )}

          <Input
            label="Nom"
            labelStyle={styles.label}
            placeholder="Entrez votre nom"
            placeholderTextColor={"#dedede"}
            onChangeText={(text) =>
              setLastname(text.charAt(0).toUpperCase() + text.slice(1))
            }
            onBlur={validateLastname}
            value={lastname}
            renderErrorMessage={isValidLastname}
          />
          {!isValidLastname && (
            <Text style={stylesProfile.errorText}>
              Le nom doit comporter au moins 1 caractères.
            </Text>
          )}

          <Text
            style={{
              color: "#888888",
              fontWeight: "400",
              paddingLeft: 10,
              fontSize: 16,
            }}
          >
            Genre
          </Text>
          <RNPickerSelect
            placeholder={{ label: "Sélectionner le genre", value: "" }}
            onValueChange={(value) => setGender(value)}
            value={gender}
            items={[
              { label: "Masculin", value: "male" },
              { label: "Feminin", value: "female" },
              { label: "Autre", value: "other" },
            ]}
          />

          <View className=" flex items-center justify-center mt-auto mb-2">
            <CustomButton
              title="Suivant"
              onPress={handleFirstSumbit}
              disabled={isFirstFormEmpty}
              color={"#9CDE00"}
            />
          </View>
        </>
      )}

      {validFirstPart && (
        <>
          {!isAllergySelectorValid && (
            <>
              <Text className=" m-4 text-gray-300 text-lg">
                {firstname} {lastname}
              </Text>
              <Text style={styles.label} className="m-2">
                Date de naissance
              </Text>
              <TouchableOpacity onPress={() => setShowDatePicker(true)}>
                {dateOfBirth && (
                  <View className="flex items-center">
                    <Text className="text-white text-center font-semibold bg-lime-400 rounded-lg w-[80%] m-4 p-2 ">
                      {formatDateToDDMMYYYY(dateOfBirth)}
                    </Text>
                  </View>
                )}
                {!dateOfBirth && (
                  <View className="flex items-center">
                    <Text className="text-white text-center font-semibold bg-blue-400 rounded-lg w-[80%] m-4 p-2 ">
                      Choisir la date de naissance
                    </Text>
                  </View>
                )}
              </TouchableOpacity>
              {showDatePicker && (
                <DateTimePicker
                  value={dateOfBirth || new Date()}
                  mode="date"
                  display="default"
                  maximumDate={new Date()}
                  onChange={(event, selectedDate) => {
                    setShowDatePicker(false);
                    if (selectedDate) {
                      setDateOfBirth(selectedDate);
                    }
                  }}
                />
              )}
              <Input
                label="Poids (kg)"
                labelStyle={styles.label}
                placeholder="Votre poids en kg"
                placeholderTextColor={"#dedede"}
                onChangeText={(text) => setWeight(parseInt(text))}
                onBlur={validateWeight}
                value={weight ? weight.toString() : ""}
                maxLength={4}
                renderErrorMessage={isValidWeight}
                keyboardType="numeric"
              ></Input>
              {!isValidWeight && (
                <Text style={stylesProfile.errorText}>
                  Le poids doit être contenu entre 1 et 999kg.
                </Text>
              )}

              <TouchableOpacity
                onPress={() => {
                  setIsAllergySelectorValid(true);
                }}
              >
                <View className="flex items-center">
                  <Text className="text-lime-400 text-center font-semibold bg-lime-100 rounded-lg w-[80%] p-1 ">
                    Choisir vos allergies médicamenteuses
                  </Text>
                </View>
              </TouchableOpacity>

              <FlatList
                className=" m-3 min-h-[40px] max-h-[40px]"
                horizontal={true}
                data={preference}
                keyExtractor={(_item, index) => index.toString()}
                renderItem={({ item }) => (
                  <View className=" bg-blue-200 m-1 p-1 rounded-lg flex flex-row justify-center align-middle">
                    <Text className=" text-blue-400">{item}</Text>
                  </View>
                )}
              />

              <View className=" flex items-center justify-center mt-auto mb-2">
                <View className=" m-3 w-max ">
                  <CustomButton
                    title="Retour"
                    onPress={handleFirstSumbit}
                    disabled={false}
                    color={"#4296E4"}
                  />
                </View>
                <CustomButton
                  title="Enregistrer le profil"
                  onPress={handleSumbit}
                  disabled={isFormEmpty}
                  color={"#9CDE00"}
                />
              </View>
            </>
          )}
          {isAllergySelectorValid && (
            <AllergySelector
              isAllergySelectorValid={handleAllergySelectorValidation}
              preference={preference}
              onPreferenceChange={setPreference}
            ></AllergySelector>
          )}
        </>
      )}
    </SafeAreaView>
  );
}

const stylesProfile = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    display: "flex",
    gap: 5,
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: "80%",
  },
  errorText: {
    color: "red",
    marginBottom: 10,
  },
});
