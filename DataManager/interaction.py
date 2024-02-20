import json
import re

def parse_interactions(text):
    change = [
        "CONTRE-INDICATION",
        "CI - ASDEC - APEC",
        "ASDEC - APEC",
        "ASDEC - PE",
        "CI - PE",
        "CI - ASDEC",
        "CI - APEC"
    ]
    for ci in change:
        text=text.replace(ci,ci.lower())

    # Split the text by the name of the substances, which are all uppercase
    substance_blocks = re.split(r'\n([A-ZÀ-ÿ][A-ZÀ-ÿ0-9 \-\'(),.;/]*[A-ZÀ-ÿ\-\'()]+)\n', text)[1:]
    
    interactions = {}
    for i in range(0, len(substance_blocks), 2):
        substance = substance_blocks[i].strip()
        details = substance_blocks[i + 1]
        for ci in change:
            details=details.replace(ci.lower(),ci)

        
        # Find all interactions for the current substance
        interaction_details = re.findall(
            r'\+\s*([A-ZÀ-ÿ][A-ZÀ-ÿ0-9\s\-\'(),.;/]+)'
            r'(Association DECONSEILLEE|Précaution d\'emploi|A prendre en compte|CONTRE-INDICATION|CI - ASDEC - APEC|ASDEC - APEC|ASDEC - PE|CI - PE|CI - ASDEC|CI - APEC)'
            r'([\s\S]+?)(?=\n\+|$)', 
            details
        )
        
        interactions_list = []
        for interaction in interaction_details:
            interacting_substance, association, detail = interaction
            interactions_list.append({
                "interacting_substance": interacting_substance.strip(),
                "association": association.strip(),
                "details": ' '.join(detail.split()).strip()  # Normalize whitespace
            })
        
        interactions[substance] = interactions_list

    return interactions

def save_interactions_to_json(interactions, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(interactions, f, ensure_ascii=False, indent=4)


text = """
ABATACEPT
+ ANTI-TNF ALPHA
Association DECONSEILLEEMajoration de l’immunodépression.
+ VACCINS VIVANTS ATTÉNUÉS
Association DECONSEILLEE
ainsi que pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée, éventuellement mortelle.
ABIRATERONE
Voir aussi : médicaments à l'origine d'un hypogonadisme masculin
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution notable des concentrations plasmatiques de
l’abiratérone, avec risque de moindre efficacité.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par l'abiratérone.
Chez l'insuffisant cardiaque, risque d'augmentation des effets
indésirables du métoprolol, par diminution de son métabolisme
hépatique par l'abiratérone.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
propafénone pendant le traitement par l'abiratérone.
Risque d'augmentation des effets indésirables de la propafénone,
par diminution de son métabolisme hépatique par l'abiratérone.
+ RIFAMPICINE
Association DECONSEILLEEDiminution notable des concentrations plasmatiques de
l’abiratérone, avec risque de moindre efficacité.
ABROCITINIB
+ FLUCONAZOLE
Précaution d'emploi
Réduire la posologie de l’abrocitinib de moitié en cas de traitement par
le fluconazole.
Risque de majoration des effets indésirables de l’abrocitinib par
diminution de son métabolisme.
+ FLUVOXAMINE
Précaution d'emploi
Réduire la posologie de l’abrocitinib de moitié en cas de traitement par
la fluvoxamine.
Risque de majoration des effets indésirables de l’abrocitinib par
diminution de son métabolisme.
ACETAZOLAMIDE
Voir aussi : alcalinisants urinaires
+ ACIDE ACETYLSALICYLIQUE
Association DECONSEILLEEMajoration des effets indésirables, et notamment de l'acidose
métabolique, de l'acide acétylsalicylique à doses élevées et de
l'acétazolamide, par diminution de l'élimination de l'acide
acétylsalicylique par l'acétazolamide.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et, si besoin, contrôle des concentrations
plasmatiques de carbamazépine et réduction éventuelle de sa
posologie.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
+ LITHIUM
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
ACIDE ACETOHYDROXAMIQUE
+ FER
A prendre en compteDiminution de l'absorption digestive de ces deux médicaments par
chélation du fer.
ACIDE ACETYLSALICYLIQUE
Voir aussi : antiagrégants plaquettaires - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ACETAZOLAMIDE
Association DECONSEILLEEMajoration des effets indésirables, et notamment de l'acidose
métabolique, de l'acide acétylsalicylique à doses élevées et de
l'acétazolamide, par diminution de l'élimination de l'acide
acétylsalicylique par l'acétazolamide.
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Pour des doses anti-inflammatoires d'acide acétylsalicylique (>= 1g
par prise et/ou >= 3g par jour) ou pour des doses antalgiques ou
antipyrétiques (>= 500 mg par prise et/ou < 3g par jour) :
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Par ailleurs, réduction de
l'effet antihypertenseur.
+ ANTICOAGULANTS ORAUX
CI - ASDEC - APEC
Contre-indication avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour) et en cas d’antécédent d’ulcère gastro-duodénal
Association déconseillée avec :
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour) en l'absence d’antécédent d’ulcère gastro-duodénal
- des doses antiagrégantes (de 50 mg à 375 mg par jour) et en cas
d’antécédent d’ulcère gastro-duodénal. Nécessité d'un contrôle le cas
échéant, en particulier du temps de saignement.
A prendre en compte avec :
- des doses antiagrégantes (de 50 mg à 375 mg par jour)
Majoration du risque hémorragique, notamment en cas
d’antécédent d’ulcère gastro-duodénal.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
ASDEC - APEC
Association déconseillée avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour)
A prendre en compte avec :
- des doses antiagrégantes (de 50 mg à 375 mg par jour en 1 ou
plusieurs prises)
Majoration du risque ulcérogène et hémorragique digestif.
+ CLOPIDOGREL
ASDEC - PE
Association déconseillée :
- en dehors des indications validées pour cette association dans les
syndromes coronariens aigus.
Précaution d'emploi :
- dans les indications validées pour cette association dans les
syndromes coronariens aigus. Surveillance clinique.
Majoration du risque hémorragique par addition des activités
antiagrégantes plaquettaires.
+ DEFERASIROX
A prendre en compte
A prendre en compte :
- Pour des doses anti-inflammatoires d'acide acétylsalicylique ( 1g par
prise et/ou 3g par jour)
- Pour des doses antalgiques ou antipyrétiques d'acide acétylsalicylique
( 500 mg par prise et/ou <3g par jour) et ( 500 mg par prise et/ou <3g
par jour)
Majoration du risque ulcérogène et hémorragique digestif.
+ DIURÉTIQUES
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Pour des doses anti-inflammatoires d'acide acétylsalicylique (>= 1g
par prise et/ou >= 3g par jour) ou pour des doses antalgiques ou
antipyrétiques (>= 500 mg par prise et/ou < 3g par jour) :
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
avec une fonction rénale altérée), par diminution de la filtration
glomérulaire secondaire à une diminution de la synthèse des
prostaglandines rénales. Par ailleurs, réduction de l'effet
antihypertenseur.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
ASDEC - APEC
Association déconseillée avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
A prendre en compte avec :
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour).
Majoration du risque hémorragique.
+ HÉPARINES (DOSES CURATIVES ET/OU SUJET ÂGÉ)
ASDEC - APEC
Association déconseillée avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour)
Utiliser un autre anti-inflammatoire ou un autre antalgique ou
antipyrétique.
A prendre en compte avec :
- des doses antiagrégantes (de 50 mg à 375 mg par jour).
Augmentation du risque hémorragique (inhibition de la fonction
plaquettaire et agression de la muqueuse gastroduodénale par
l’acide acétylsalicylique.
+ HÉPARINES (DOSES PRÉVENTIVES)
A prendre en compteL’utilisation conjointe de médicaments agissant à divers niveaux de
l’hémostase majore le risque de saignement. Ainsi, chez le sujet de
moins de 65 ans, l’association de l'héparine à doses préventives,
ou de substances apparentées, à l’acide acétylsalicylique, quelle
que soit la dose, doit être prise en compte en maintenant une
surveillance clinique et éventuellement biologique.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Pour des doses anti-inflammatoires d'acide acétylsalicylique (>= 1g
par prise et/ou >= 3g par jour) ou pour des doses antalgiques ou
antipyrétiques (>= 500 mg par prise et/ou < 3g par jour) :
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Par ailleurs, réduction de
l'effet antihypertenseur.
+ METHOTREXATE
CI - PE
Avec le méthotrexate utilisé à des doses > 20 mg/semaine :
- contre-indication avec l'acide acétylsalicylique utilisé à doses
antalgiques, antipyrétiques ou anti-inflammatoires
- précaution d'emploi avec des doses antiagrégantes plaquettaires
d'acide acétylsalicylique. Contrôle hebdomadaire de l’hémogramme
durant les premières semaines de l’association. Surveillance accrue en
cas d’altération (même légère) de la fonction rénale, ainsi que chez le
sujet âgé.
Avec le méthotrexate utilisé à des doses =< 20 mg/semaine :
- précaution d'emploi avec l'acide acétylsalicylique utilisé à doses
antalgiques, antipyrétiques ou anti-inflammatoires. Contrôle
hebdomadaire de l’hémogramme durant les premières semaines de
l’association. Surveillance accrue en cas d’altération (même légère) de
la fonction rénale, ainsi que chez le sujet âgé.
Majoration de la toxicité, notamment hématologique, du
méthotrexate (diminution de sa clairance rénale par l'acide
acétylsalicylique).
+ NICORANDIL
Association DECONSEILLEEMajoration du risque ulcérogène et hémorragique digestif.
+ PEMETREXED
ASDEC - PE
Association déconseillée :
- en cas de fonction rénale faible à modérée .
Précaution d'emploi :
- en cas de fonction rénale normale. Surveillance biologique de la
fonction rénale.
Risque de majoration de la toxicité du pemetrexed (diminution de
sa clairance rénale par l’acide acétylsalicylique à doses anti-
inflammatoires).
+ PROBENECIDE
Association DECONSEILLEEDiminution de l’effet uricosurique par compétition de l’élimination de
l’acide urique au niveau des tubules rénaux.
+ TICAGRELOR
ASDEC - PE
Association déconseillée :
- en dehors des indications validées pour cette association dans les
syndromes coronariens aigus.
Précaution d'emploi :
- dans les indications validées pour cette association dans les
syndromes coronariens aigus. Surveillance clinique.
Majoration du risque hémorragique par addition des activités
antiagrégantes plaquettaires.
+ TICLOPIDINE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Majoration du risque hémorragique par addition des activités
antiagrégantes plaquettaires.
ACIDE ASCORBIQUE
+ CICLOSPORINE
A prendre en compteRisque de diminution des concentrations sanguines de la
ciclosporine, notamment en cas d’association avec la vitamine E.
+ DÉFÉRIPRONE
Précaution d'emploiPar extrapolation à partir de l’interaction avec la déféroxamine :
avec l’acide ascorbique à fortes doses et par voie IV, risque
d’anomalies de la fonction cardiaque, voire insuffisance cardiaque
aiguë (en général réversible à l’arrêt de la vitamine C).
+ DÉFÉROXAMINE
Précaution d'emploi
En cas d'hémochromatose, ne donner de la vitamine C qu'après avoir
commencé le traitement par la déféroxamine. Surveiller la fonction
cardiaque en cas d'association.
Avec l'acide ascorbique à fortes doses et par voie IV : anomalies de
la fonction cardiaque, voire insuffisance cardiaque aiguë (en
général réversible à l'arrêt de la vitamine C).
ACIDE CHOLIQUE
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
CONTRE-INDICATIONEffet antagoniste du barbiturique.
ACIDE CLODRONIQUE
Voir aussi : bisphosphonates - médicaments néphrotoxiques - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ESTRAMUSTINE
Précaution d'emploi
Surveillance clinique au cours de l’association.
Risque d’augmentation des concentrations plasmatiques
d’estramustine par le clodronate.
ACIDE FOLINIQUE
Voir aussi : folates
+ FLUOROURACILE (ET, PAR EXTRAPOLATION, AUTRES FLUOROPYRIMIDINES)
A prendre en comptePotentialisation des effets, à la fois cytostatiques et indésirables, du
fluoro-uracile.
ACIDE FUSIDIQUE
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
CONTRE-INDICATION
Arrêter le traitement par l'inhibiteur de l'HMG Co-A
réductase avant d'initier un traitement par acide fusidique ou utiliser un
autre antibiotique.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'acide fusidique
par diminution de son métabolisme hépatique par la bithérapie.
ACIDE NICOTINIQUE
+ ALCOOL (BOISSON OU EXCIPIENT)
A prendre en compteRisque de prurit, de rougeur et de chaleur, lié à une potentialisation
de l'effet vasodilatateur.
ACIDE URSODESOXYCHOLIQUE
+ CICLOSPORINE
A prendre en compteRisque de variation des concentrations sanguines de ciclosporine.
ACITRETINE
Voir aussi : rétinoïdes
+ ALCOOL (BOISSON OU EXCIPIENT)
CONTRE-INDICATIONChez la femme en âge de procréer, risque de transformation de
l’acitrétine en étrétinate, puissant tératogène dont la demi-vie très
prolongée (120 jours) expose à un risque tératogène majeur en cas
de grossesse, pendant le traitement et les 2 mois suivant son arrêt.
+ METHOTREXATE
CONTRE-INDICATIONRisque de majoration de l'hépatotoxicité du méthotrexate.
ADRÉNALINE (VOIE BUCCO-DENTAIRE OU SOUS-CUTANÉE)
(adrenaline
+ ANESTHÉSIQUES VOLATILS HALOGÉNÉS
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ ANTIDÉPRESSEURS IMIPRAMINIQUES
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ IMAO IRRÉVERSIBLES
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
AFATINIB
+ AMIODARONE
Précaution d'emploi
Il est recommandé d’administrer l'amiodarone le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatiques d’afatinib par
augmentation de son absorption par l'amiodarone.
+ CICLOSPORINE
Précaution d'emploi
Il est recommandé d’administrer la ciclosporine le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par la ciclosporine.
+ ERYTHROMYCINE
Précaution d'emploi
Il est recommandé d’administrer l'érythromycine le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par l'érythromycine.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique pendant l’association et 1 à 2 semaines après leur
arrêt.
Diminution des concentrations plasmatiques de l’afatinib par
augmentation de son métabolisme par ces substances.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Il est recommandé d’administrer l'inhibiteur de protéases le plus à
distance possible de l’afatinib, en respectant de préférence un
intervalle de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatiques d’afatinib par
augmentation de son absorption par l'inhibiteur de protéases.
+ ITRACONAZOLE
Précaution d'emploi
Il est recommandé d’administrer l'itraconazole le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par l'itraconazole.
+ KETOCONAZOLE
Précaution d'emploi
Il est recommandé d’administrer le kétoconazole le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par le kétoconazole.
+ PRIMIDONE
Précaution d'emploi
Surveillance clinique pendant l’association et 1 à 2 semaines après leur
arrêt.
Diminution des concentrations plasmatiques de l’afatinib par
augmentation de son métabolisme par la primidone.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique pendant l’association et 1 à 2 semaines après leur
arrêt.
Diminution des concentrations plasmatiques de l’afatinib par
augmentation de son métabolisme par la rifampicine.
+ VERAPAMIL
Précaution d'emploi
Il est recommandé d’administrer le vérapamil le plus à distance possible
de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par le vérapamil.
AGOMELATINE
Voir aussi : médicaments sédatifs
+ CIPROFLOXACINE
Association DECONSEILLEEAugmentation des concentrations d'agomélatine, avec risque de
majoration des effets indésirables.
+ FLUVOXAMINE
CONTRE-INDICATIONAugmentation des concentrations d'agomélatine, avec risque de
majoration des effets indésirables.
ALBENDAZOLE
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique de la réponse thérapeutique et adaptation
éventuelle de la posologie de l’albendazole pendant le traitement avec
l’inducteur enzymatique et après son arrêt.
Diminution importante des concentrations plasmatiques de
l’albendazole et de son métabolite actif par l’inducteur, avec risque
de baisse de son efficacité.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique de la réponse thérapeutique et adaptation
éventuelle de la posologie de l’albendazole pendant le traitement avec
l’inducteur enzymatique et après son arrêt.
Diminution importante des concentrations plasmatiques de
l’albendazole et de son métabolite actif par le ritonavir, avec risque
de baisse de son efficacité.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique de la réponse thérapeutique et adaptation
éventuelle de la posologie de l’albendazole pendant le traitement avec
l’inducteur enzymatique et après son arrêt.
Diminution importante des concentrations plasmatiques de
l’albendazole et de son métabolite actif par l’inducteur, avec risque
de baisse de son efficacité.
ALCALINISANTS URINAIRES
(acetazolamide, sodium (bicarbonate de), trometamol)
+ HYDROQUINIDINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations de l'hydroquinidine ; si besoin, adaptation de la
posologie pendant le traitement alcalinisant et après son arrêt.
Augmentation des concentrations plasmatiques de l'hydroquinidine
et risque de surdosage (diminution de l'excrétion rénale de
l'hydroquinidine par alcalinisation des urines).
+ QUINIDINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle de la
quinidinémie ; si besoin, adaptation de la posologie pendant le
traitement alcalinisant et après son arrêt.
Augmentation des concentrations plasmatiques de la quinidine et
risque de surdosage (diminution de l'excrétion rénale de la
quinidine par alcalinisation des urines).
ALCALOÏDES DE L'ERGOT DE SEIGLE DOPAMINERGIQUES
(bromocriptine, cabergoline, lisuride)
+ ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ ANTIPARKINSONIENS ANTICHOLINERGIQUES
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de majoration des troubles neuropsychiques.
+ MACROLIDES (SAUF SPIRAMYCINE)
Association DECONSEILLEEAugmentation des concentrations plasmatiques du dopaminergique
avec accroissement possible de son activité ou apparition de
signes de surdosage.
+ SYMPATHOMIMÉTIQUES ALPHA (VOIES ORALE ET/OU NASALE)
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ SYMPATHOMIMÉTIQUES INDIRECTS
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
(dihydroergotamine, ergotamine, méthylergométrine)
+ ALCALOÏDES DE L'ERGOT DE SEIGLE DOPAMINERGIQUES
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONRisque de vasoconstriction coronaire ou des extrémités
(ergotisme), ou de poussées hypertensives.
+ LÉTERMOVIR
CONTRE-INDICATIONRisque de vasoconstriction coronaire ou des extrémités
(ergotisme), ou de poussées hypertensives.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'alcaloïde de
l'ergot de seigle vasoconstricteur par diminution de son
métabolisme hépatique par la bithérapie.
+ SYMPATHOMIMÉTIQUES ALPHA (VOIES ORALE ET/OU NASALE)
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ SYMPATHOMIMÉTIQUES INDIRECTS
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ TRIPTANS
CONTRE-INDICATION
Respecter un délai de 6 à 24 heures, selon le triptan, entre la prise de
celui-ci et celle de l'alcaloïde ergoté
Risque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
ALCOOL (BOISSON OU EXCIPIENT)
(anpu
+ ACIDE NICOTINIQUE
A prendre en compteRisque de prurit, de rougeur et de chaleur, lié à une potentialisation
de l'effet vasodilatateur.
+ ACITRETINE
CONTRE-INDICATIONChez la femme en âge de procréer, risque de transformation de
l’acitrétine en étrétinate, puissant tératogène dont la demi-vie très
prolongée (120 jours) expose à un risque tératogène majeur en cas
de grossesse, pendant le traitement et les 2 mois suivant son arrêt.
+ ANTABUSE (RÉACTION)
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool. Tenir compte de l’élimination complète des médicaments en se
référant à leur demi-vie avant la reprise de boissons alcoolisées ou du
médicament contenant de l’alcool.
Effet antabuse (chaleur, rougeurs, vomissements, tachycardie).
+ IMAO IRRÉVERSIBLES
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Majoration des effets hypertenseurs et/ou hyperthermiques de la
tyramine présente dans certaines boissons alcoolisées (chianti,
certaines bières, etc).
+ INSULINE
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Augmentation de la réaction hypoglycémique (inhibition des
réactions de compensation pouvant faciliter la survenue de coma
hypoglycémique).
+ MÉDICAMENTS SÉDATIFS
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Majoration par l'alcool de l'effet sédatif de ces substances.
L'altération de la vigilance peut rendre dangereuses la conduite de
véhicules et l'utilisation de machines.
+ METFORMINE
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Risque majoré d'acidose lactique lors d'intoxication alcoolique
aiguë, particulièrement en cas de jeûne ou dénutrition, ou bien
d'insuffisance hépatocellulaire.
+ SULFAMIDES HYPOGLYCÉMIANTS
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Effet antabuse, notamment pour glibenclamide, glipizide,
tolbutamide. Augmentation de la réaction hypoglycémique
(inhibition des réactions de compensation) pouvant faciliter la
survenue de coma hypoglycémique.
ALDESLEUKINE
+ PRODUITS DE CONTRASTE IODÉS
A prendre en compteMajoration du risque de réaction aux produits de contraste en cas
de traitement antérieur par interleukine 2 : éruption cutanée ou plus
rarement hypotension, oligurie voire insuffisance rénale.
ALFENTANIL
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier III - morphiniques - médicaments sédatifs - substrats à risque du CYP3A4
+ CIMETIDINE
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par la
cimétidine.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de l'effet dépresseur respiratoire de
l'analgésique opiacé par diminution de son métabolisme hépatique.
+ DILTIAZEM
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par le diltiazem.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
+ ERYTHROMYCINE
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par
l'érythromycine.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
+ FLUCONAZOLE
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par le
fluconazole.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’analgésique
opiacé en cas de traitement par un inhibiteur puissant du CYP3A4.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
ALFUZOSINE
Voir aussi : alphabloquants à visée urologique - médicaments à l'origine d'une hypotension orthostatique
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de
l’alfuzosine et de ses effets indésirables.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'afuzosine par
diminution de son métabolisme hépatique par la bithérapie.
ALLOPURINOL
Voir aussi : inhibiteurs de la xanthine oxydase
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'allopurinol et 8 jours après
son arrêt.
Augmentation du risque hémorragique.
+ DIDANOSINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de didanosine et
de ses effets indésirables.
+ PÉNICILLINES A
A prendre en compteRisque accru de réactions cutanées.
+ VIDARABINE
Association DECONSEILLEERisque accru de troubles neurologiques (tremblements, confusion)
par inhibition partielle du métabolisme de l'antiviral.
ALPHABLOQUANTS À VISÉE UROLOGIQUE
(alfuzosine, doxazosine, prazosine, silodosine, tamsulosine, terazosine)
+ ANTIHYPERTENSEURS ALPHA-BLOQUANTS
Association DECONSEILLEEMajoration de l'effet hypotenseur. Risque d'hypotension
orthostatique sévère.
+ ANTIHYPERTENSEURS SAUF ALPHA-BLOQUANTS
A prendre en compteMajoration de l'effet hypotenseur. Risque d'hypotension
orthostatique majoré.
+ INHIBITEURS DE LA PHOSPHODIESTERASE DE TYPE 5
ASDEC - PE
Association déconseillée :
- avec la doxazosine
Précaution d'emploi :
- avec les autres alpha-bloquants
Débuter le traitement aux posologies minimales recommandées et
adapter progressivement les doses si besoin.
Risque d’hypotension orthostatique, notamment chez le sujet âgé.
ALPRAZOLAM
Voir aussi : benzodiazépines et apparentés - médicaments sédatifs
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en comptePossible augmentation de l'effet sédatif de l'alprazolam.
ALUMINIUM (SELS)
(gel d'hydroxyde d'aluminium et de carbonate de magnesium codesseches, hydrotalcite, magaldrate, oxyde d'aluminium, phosphate d'aluminium)
+ CITRATES
Précaution d'emploi
Prendre les topiques gastro-intestinaux à base d'aluminium à distance
des citrates (plus de 2 heures si possible), y compris les citrates
naturels (jus d'agrumes).
Risque de facilitation du passage systémique de l’aluminium,
notamment en cas de fonction rénale altérée.
AMBRISENTAN
+ CICLOSPORINE
A prendre en compteDoublement des concentrations d’ambrisentan, avec majoration de
l’effet vasodilatateur (céphalées).
AMINOSIDES
(amikacine, gentamicine, isepamicine, netilmicine, streptomycine, tobramycine)
+ AUTRES AMINOSIDES
CI - APEC
Contre-indication :
- en cas d'administration simultanée
A prendre en compte :
- en cas d'administrations successives
Risque accru de néphrotoxicité et d'ototoxicité (l'ototoxicité est
cumulative en cas d'administrations successives).
+ AMPHOTERICINE B
A prendre en compteAvec l'amphotéricine B administrée par voie IV : risque accru de
néphrotoxicité.
+ ATALUREN
CONTRE-INDICATIONRisque de potentialisation de la toxicité rénale de l’aminoside.
+ BOTULIQUE (TOXINE)
Association DECONSEILLEE
Utiliser un autre antibiotique.
Risque d'augmentation des effets de la toxine botulique avec les
aminosides (par extrapolation à partir des effets observés au cours
du botulisme).
+ CEFALOTINE
Précaution d'emploi
Surveillance de la fonction rénale.
L'augmentation de la néphrotoxicité des aminosides par la
céfalotine est discutée.
+ CICLOSPORINE
A prendre en compteAugmentation de la créatininémie plus importante que sous
ciclosporine seule, avec majoration du risque néphrotoxique.
+ CURARES
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
+ DIURÉTIQUES DE L'ANSE
Précaution d'emploi
Association possible sous contrôle de l'état d'hydratation, des fonctions
rénale et cochléovestibulaire, et éventuellement, des concentrations
plasmatiques de l'aminoside.
Augmentation des risques néphrotoxiques et ototoxiques de
l'aminoside (insuffisance rénale fonctionnelle liée à la
déshydratation entraînée par le diurétique).
+ ORGANOPLATINES
A prendre en compteAddition des effets néphrotoxiques et/ou ototoxiques, notamment
en cas d'insuffisance rénale préalable.
+ POLYMYXINE B
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance stricte avec une
justification bactériologique indiscutable.
Addition des effets néphrotoxiques.
+ TACROLIMUS
A prendre en compteAugmentation de la créatininémie plus importante que sous
tacrolimus seul (synergie des effets néphrotoxiques des deux
substances).
AMIODARONE
Voir aussi : antiarythmiques - bradycardisants - substances susceptibles de donner des torsades de pointes - torsadogènes (sauf arsénieux, antiparasitaires,
neuroleptiques, méthadone...)
+ AFATINIB
Précaution d'emploi
Il est recommandé d’administrer l'amiodarone le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatiques d’afatinib par
augmentation de son absorption par l'amiodarone.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'amiodarone et jusqu'à 4
semaines après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL ET SOTALOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de l'automatisme et de la conduction (suppression des
mécanismes sympathiques compensateurs).
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Précaution d'emploi
Surveillance clinique et ECG régulière.
Troubles de l'automatisme et de la conduction cardiaque avec
risque de bradycardie excessive.
+ CICLOSPORINE
Association DECONSEILLEE
Dosage des concentrations sanguines de ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie de la ciclosporine pendant
le traitement par l'amiodarone.
Augmentation des concentrations sanguines de ciclosporine, par
diminution de son métabolisme hépatique, avec risque d'effets
néphrotoxiques.
+ COBICISTAT
CONTRE-INDICATIONRisque de majoration des effets indésirables de l'amiodarone par
diminution de son métabolisme par le cobicistat.
+ DABIGATRAN
Précaution d'emploi
Dans l'indication post-chirurgicale : surveillance clinique et adaptation
de la posologie du dabigatran si nécessaire, sans excéder 150 mg/j.
Augmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique, ECG et, s'il y a lieu, contrôle de la digoxinémie et
adaptation de la posologie de la digoxine.
Dépression de l'automatisme (bradycardie excessive) et troubles
de la conduction auriculo-ventriculaire. De plus, augmentation de la
digoxinémie par diminution de la clairance de la digoxine.
+ DILTIAZEM
ASDEC - PE
Association déconseillée avec :
- le diltiazem IV
Si l'association ne peut être évitée, surveillance clinique et ECG continu.
Précaution d'emploi avec :
- le diltiazem per os
Surveillance clinique et ECG.
Pour diltiazem voie injectable : risque de bradycardie et de bloc
auriculo-ventriculaire
Pour diltiazem per os : risque de bradycardie ou de bloc auriculo-
ventriculaire, notamment chez les personnes âgées.
+ DOCETAXEL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
docétaxel.
Risque de majoration des effets indésirables du docétaxel par
diminution de son métabolisme hépatique par l’amiodarone
+ ESMOLOL
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ FIDAXOMICINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ FLUCONAZOLE
Précaution d'emploi
Surveillance clinique, particulièrement aux fortes doses de fluconazole
(800 mg/j).
Risque d’allongement de l’intervalle QT.
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d'augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par l’amiodarone.
+ LIDOCAINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations plasmatiques de lidocaïne. Si besoin, adaptation de la
posologie de la lidocaïne pendant le traitement par amiodarone et après
son arrêt.
Risque d’augmentation des concentrations plasmatiques de
lidocaïne, avec possibilité d’effets indésirables neurologiques et
cardiaques, par diminution de son métabolisme hépatique par
l’amiodarone.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'amiodarone.
+ OLAPARIB
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg 2
fois par jour avec l’amiodarone.
Augmentation des concentrations plasmatiques d’olaparib par l'
amiodarone
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'amiodarone
par diminution de son métabolisme hépatique par la bithérapie.
+ ORLISTAT
Précaution d'emploi
Surveillance clinique et, si besoin, ECG.
Risque de diminution des concentrations plasmatiques de
l'amiodarone et de son métabolite actif.
+ PACLITAXEL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
paclitaxel.
Risque de majoration des effets indésirables du paclitaxel par
diminution de son métabolisme hépatique par l’amiodarone.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Association DECONSEILLEEMajoration du risque de troubles du rythme ventriculaire par
potentialisation des effets antiarythmiques, ainsi que des effets
indésirables neurologiques, par diminution du métabolisme
hépatique de la phénytoïne par l’amiodarone.
+ SIMVASTATINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
simvastatine).
+ SOFOSBUVIR
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique et ECG étroite,
en particulier pendant les premières semaines de traitement. Une
surveillance continue en milieu hospitalier est requise pendant les 48
heures qui suivent la co-adminsitration.
Prendre en compte la longue demi-vie de l'amiodarone chez les
patients l'ayant arrêtée au cours des derniers mois et qui doivent
débuter un traitement contenant du sofosbuvir.
Survenue de bradycardie éventuellement brutale, pouvant avoir des
conséquences fatales.
+ TACROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines de tacrolimus, contrôle de la
fonction rénale et adaptation de la posologie de tacrolimus pendant
l’association et à l’arrêt de l’amiodarone.
Augmentation des concentrations sanguines de tacrolimus par
inhibition de son métabolisme par l’amiodarone.
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ TAMSULOSINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la tamsulosine
pendant le traitement par l’inhibiteur enzymatique et après son arrêt, le
cas échéant.
Risque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
+ TOLVAPTAN
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
+ VÉNÉTOCLAX
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment hématologique,
et adaptation de la posologie du vénétoclax.
Risque d’augmentation des effets indésirables du vénétoclax par
diminution de son métabolisme hépatique.
+ VERAPAMIL
ASDEC - PE
Association déconseillée avec :
- le vérapamil IV
Si l'association ne peut être évitée, surveillance clinique et ECG continu.
Précaution d'emploi avec :
- le vérapamil per os
Surveillance clinique et ECG.
Pour vérapamil voie injectable :
-risque de bradycardie ou de bloc auriculo-ventriculaire.
Pour vérapamil per os :
-risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez les personnes âgées.
+ VORICONAZOLE
Précaution d'emploi
Surveillance clinique et ECG, et adaptation éventuelle de la posologie
de l’amiodarone.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes, par possible diminution du métabolisme de
l’amiodarone.
AMLODIPINE
Voir aussi : antagonistes des canaux calciques - antihypertenseurs sauf alpha-bloquants - dihydropyridines - médicaments abaissant la pression artérielle
+ SIMVASTATINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
AMPHOTERICINE B
Voir aussi : hypokaliémiants - médicaments néphrotoxiques
+ AMINOSIDES
A prendre en compteAvec l'amphotéricine B administrée par voie IV : risque accru de
néphrotoxicité.
+ CICLOSPORINE
A prendre en compteAvec l'amphotéricine B administrée par voie IV : augmentation de
la créatininémie plus importante que sous ciclosporine seule
(synergie des effets néphrotoxiques des deux substances).
+ TACROLIMUS
A prendre en compteAvec l'amphotéricine B administrée par voie IV : augmentation de
la créatininémie plus importante que sous tacrolimus seul (synergie
des effets néphrotoxiques des deux substances).
+ ZIDOVUDINE
Précaution d'emploi
Contrôle plus fréquent de l'hémogramme.
Avec l'amphotéricine B administrée par voie IV : augmentation de
la toxicité hématologique (addition d'effets de toxicité médullaire).
ANAGRELIDE
+ ANTIAGRÉGANTS PLAQUETTAIRES
Association DECONSEILLEEMajoration des événements hémorragiques.
+ OMEPRAZOLE
A prendre en compte
Préférer un autre inhibiteur de la pompe à protons.
Risque de moindre efficacité de l'anagrélide par augmentation de
son métabolisme par l'oméprazole.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
ANAKINRA
+ ANTI-TNF ALPHA
Association DECONSEILLEERisque accru d'infections graves et de neutropénies.
+ ETANERCEPT
Association DECONSEILLEERisque accru d'infections graves et de neutropénies.
ANALGÉSIQUES MORPHINIQUES AGONISTES
(alfentanil, codeine, dihydrocodeine, fentanyl, hydromorphone, morphine, oxycodone, pethidine, remifentanil, sufentanil, tapentadol, tramadol)
+ AUTRES ANALGÉSIQUES MORPHINIQUES AGONISTES
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ ANTITUSSIFS MORPHINE-LIKE
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ ANTITUSSIFS MORPHINIQUES VRAIS
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
ANALGÉSIQUES MORPHINIQUES DE PALIER II
(codeine, dihydrocodeine, tapentadol, tramadol)
+ MORPHINIQUES AGONISTES-ANTAGONISTES
Association DECONSEILLEEDiminution de l'effet antalgique par blocage compétitif des
récepteurs, avec risque d'apparition d'un syndrome de sevrage.
+ MORPHINIQUES ANTAGONISTES PARTIELS
Association DECONSEILLEERisque de diminution de l’effet antalgique.
ANALGÉSIQUES MORPHINIQUES DE PALIER III
(alfentanil, fentanyl, hydromorphone, morphine, oxycodone, pethidine, remifentanil, sufentanil)
+ MORPHINIQUES AGONISTES-ANTAGONISTES
CONTRE-INDICATIONDiminution de l'effet antalgique par blocage compétitif des
récepteurs, avec risque d'apparition d'un syndrome de sevrage.
+ MORPHINIQUES ANTAGONISTES PARTIELS
CONTRE-INDICATIONRisque de diminution de l’effet antalgique.
ANALOGUES DE LA SOMATOSTATINE
(lanreotide, octreotide, pasiréotide)
+ CICLOSPORINE
Précaution d'emploi
Augmentation des doses de ciclosporine sous contrôle des
concentrations plasmatiques et réduction de la posologie après l'arrêt
du traitement par l'analogue de la somatostatine.
Avec la ciclosporine administrée par voie orale : baisse des
concentrations sanguines de ciclosporine (diminution de son
absorption intestinale).
+ INSULINE
Précaution d'emploi
Prévenir le patient du risque d'hypoglycémie ou d'hyperglycémie,
renforcer l'autosurveillance glycémique et adapter si besoin la posologie
de l'insuline pendant le traitement par l'analogue de la somatostatine.
Risque d'hypoglycémie ou d'hyperglycémie : diminution ou
augmentation des besoins en insuline, par diminution ou
augmentation de la sécrétion de glucagon endogène.
+ REPAGLINIDE
Précaution d'emploi
Renforcer l'autosurveillance glycémique et adapter si besoin la
posologie de la repaglidine pendant le traitement par l'analogue de la
somatostatine.
Risque d'hypoglycémie ou d'hyperglycémie : diminution ou
augmentation des besoins en repaglidine, par diminution ou
augmentation de la sécrétion de glucagon endogène.
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Renforcer l'autosurveillance glycémique et adapter si besoin la
posologie du sulfamide hypoglycemiant pendant le traitement par
l'analogue de la somatostatine.
Risque d'hypoglycémie ou d'hyperglycémie : diminution ou
augmentation des besoins en sulfamide hypoglycemiant, par
diminution ou augmentation de la sécrétion de glucagon endogène.
ANDROGÈNES
(androstanolone, norethandrolone, testosterone)
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation de la posologie de
l’antivitamine K pendant le traitement par l'androgène et après son arrêt.
Augmentation du risque hémorragique par effet direct sur la
coagulation et/ou les systèmes fibrinolytiques.
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Surveillance clinique et biologique pendant l’association et 1 à 2
semaines après l’arrêt de l’inducteur.
Risque de diminution des concentrations plasmatiques de
l'androgène et par conséquent de son efficacité, par augmentation
de son métabolisme hépatique par l’inducteur.
ANESTHÉSIQUES VOLATILS HALOGÉNÉS
(desflurane, halothane, isoflurane, methoxyflurane, sevoflurane)
+ ADRÉNALINE (VOIE BUCCO-DENTAIRE OU SOUS-CUTANÉE)
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
En règle générale, ne pas arrêter le traitement bêta-bloquant et, de
toute façon, éviter l'arrêt brutal. Informer l'anesthésiste de ce traitement.
Réduction des réactions cardiovasculaires de compensation par les
bêta-bloquants. L'inhibition bêta-adrénergique peut être levée
durant l'intervention par les bêta-mimétiques.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Précaution d'emploi
En règle générale, ne pas arrêter le traitement bêta-bloquant et, de
toute façon, éviter l'arrêt brutal. Informer l'anesthésiste de ce traitement.
Réduction des réactions cardiovasculaires de compensation par les
bêta-bloquants. L'inhibition bêta-adrénergique peut être levée
durant l'intervention par les bêta-stimulants.
+ ISONIAZIDE
Précaution d'emploi
En cas d'intervention programmée, arrêter, par prudence, le traitement
par l'isoniazide une semaine avant l'intervention et ne le reprendre que
15 jours après.
Potentialisation de l'effet hépatotoxique de l'isonazide, avec
formation accrue de métabolites toxiques de l'isoniazide.
+ ISOPRENALINE
Association DECONSEILLEETroubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ SYMPATHOMIMÉTIQUES ALPHA ET BÊTA (VOIE IM ET IV)
A prendre en compteDécrit avec l'halothane et le cyclopropane.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ SYMPATHOMIMÉTIQUES INDIRECTS
Précaution d'emploi
En cas d'intervention programmée, il est préférable d'interrompre le
traitement quelques jours avant l'intervention.
Poussée hypertensive peropératoire.
ANTABUSE (RÉACTION)
Les médicaments provoquant une réaction antabuse avec l’alcool sont nombreux, et leur association avec l’alcool est déconseillée.
(cefamandole, disulfirame, glibenclamide, glipizide, griseofulvine, ketoconazole, metronidazole, ornidazole, procarbazine, secnidazole, tenonitrozole, tinidazole)
+ ALCOOL (BOISSON OU EXCIPIENT)
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool. Tenir compte de l’élimination complète des médicaments en se
référant à leur demi-vie avant la reprise de boissons alcoolisées ou du
médicament contenant de l’alcool.
Effet antabuse (chaleur, rougeurs, vomissements, tachycardie).
ANTAGONISTES DES CANAUX CALCIQUES
(amlodipine, clévidipine, diltiazem, felodipine, isradipine, lacidipine, lercanidipine, manidipine, nicardipine, nifedipine, nimodipine, nitrendipine, verapamil)
+ IDÉLALISIB
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’antagoniste
calcique pendant le traitement par l’idélalisib et après son arrêt.
Majoration des effets indésirables de l’antagoniste des canaux
calciques, à type d’hypotension orthostatique, notamment chez le
sujet âgé.
17
+ INDUCTEURS ENZYMATIQUES PUISSANTS
ASDEC - PE
Association déconseillée avec la nimodipine
Précaution d'emploi :
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par l'inducteur et après
son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique.
+ INHIBITEURS PUISSANTS DU CYP3A4
ASDEC - PE
Association déconseillée:
- avec la lercanidipine.
Précaution d'emploi:
- avec les autres antagonistes des canaux calciques.
Surveillance clinique et adaptation posologique pendant le traitement
par l’inhibiteur enzymatique et après son arrêt.
Majoration des effets indésirables de l’antagoniste des canaux
calciques, le plus souvent à type d'hypotension et d'oedèmes,
notamment chez le sujet âgé.
+ RIFAMPICINE
ASDEC - PE
Association déconseillée avec la nimodipine
Précaution d'emploi :
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par la rifampicine et
après son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique.
ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
(azilsartan, candesartan cilexetil, eprosartan, irbesartan, losartan, olmesartan, telmisartan, valsartan)
+ ACIDE ACETYLSALICYLIQUE
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Pour des doses anti-inflammatoires d'acide acétylsalicylique (>= 1g
par prise et/ou >= 3g par jour) ou pour des doses antalgiques ou
antipyrétiques (>= 500 mg par prise et/ou < 3g par jour) :
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Par ailleurs, réduction de
l'effet antihypertenseur.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Insuffisance rénale aiguë chez le patient à risque (sujet âgé,
déshydratation, traitement associé avec diurétiques, altération de la
fonction rénale), par diminution de la filtration glomérulaire
secondaire à une diminution de la synthèse des prostaglandines
rénales. Ces effets sont généralement réversibles. Par ailleurs,
réduction de l’effet antihypertenseur.
+ DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
ASDEC - PE
Association déconseillée :
- si l'association est justifiée, contrôle strict de la kaliémie et de la
fonction rénale.
Précaution d'emploi :
- pour la spironolactone à des doses comprises entre 12,5 mg et 50
mg/jour, et pour l’éplérénone utilisées dans le traitement de
l'insuffisance cardiaque, ainsi qu'en cas d'hypokaliémie : contrôle strict
de la kaliémie et de la fonction rénale.
Risque d'hyperkaliémie (potentiellement létale) surtout en cas
d'insuffisance rénale (addition des effets hyperkaliémiants).
+ DIURÉTIQUES HYPOKALIÉMIANTS
Précaution d'emploi
Dans l'hypertension artérielle, lorsqu'un traitement diurétique préalable
a pu entraîner une déplétion hydrosodée, il faut :
- soit arrêter le diurétique avant de débuter le traitement par
l'antagoniste de l'angiotensine II, et réintroduire un diurétique
hypokaliémiant si nécessaire ultérieurement ;
- soit administrer des doses initiales réduites d'antagoniste de
l'angiotensine II et augmenter progressivement la posologie.
Dans tous les cas : surveiller la fonction rénale (créatininémie) dans les
premières semaines du traitement par l'antagoniste de l'angiotensine II.
Risque d'hypotension artérielle brutale et/ou d'insuffisance rénale
aiguë lors de l'instauration ou de l'augmentation de la posologie
d'un traitement par un antagoniste de l'angiotensine II en cas de
déplétion hydrosodée préexistante.
+ EPLERENONE
Précaution d'emploi
Contrôle strict de la kaliémie et de la fonction rénale pendant
l’association.
Majoration du risque d’hyperkaliémie, notamment chez le sujet âgé.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
A prendre en compteDans les indications où cette association est possible, risque accru
de dégradation de la fonction rénale, voire insuffisance rénale
aiguë, et majoration de l'hyperkaliémie, ainsi que de l'hypotension
et des syncopes.
18
+ LITHIUM
Association DECONSEILLEE
Si l'usage d'un antagoniste de l'angiotensine II est indispensable,
surveillance stricte de la lithémie et adaptation de la posologie.
Augmentation de la lithémie pouvant atteindre des valeurs toxiques
(diminution de l'excrétion rénale du lithium).
+ POTASSIUM
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (addition
des effets hyperkaliémiants).
ANTIAGRÉGANTS PLAQUETTAIRES
Plusieurs substances sont impliquées dans des interactions, du fait de leurs propriétés antiagrégantes plaquettaires.
L’utilisation de plusieurs antiagrégants plaquettaires majore le risque de saignement, de même que leur association à l’héparine et aux molécules apparentées, aux
anticoagulants oraux et aux thrombolytiques, et doit être prise en compte en maintenant une surveillance clinique régulière.
Pour l'acide acétylsalicylique, se reporter aux interactions qui lui sont propres.
(abciximab (c 7e3b fab), acide acetylsalicylique, cangrélor, caplacizumab, clopidogrel, epoprostenol, eptifibatide, iloprost, iloprost trometamol, prasugrel, proteine c
activee recombinante, proteine c humaine, ticagrelor, ticlopidine, tirofiban, treprostinil)
+ ANAGRELIDE
Association DECONSEILLEEMajoration des événements hémorragiques.
+ ANTICOAGULANTS ORAUX
A prendre en compteAugmentation du risque hémorragique.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
A prendre en compteAugmentation du risque hémorragique, notamment gastro-intestinal.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ DÉFIBROTIDE
Association DECONSEILLEERisque hémorragique accru.
+ HÉPARINES
A prendre en compteAugmentation du risque hémorragique.
+ IBRUTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteAugmentation du risque hémorragique.
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
A prendre en compteAugmentation du risque hémorragique.
+ THROMBOLYTIQUES
A prendre en compteAugmentation du risque hémorragique.
19
ANTIARYTHMIQUES
De nombreux antiarythmiques sont dépresseurs de l’automatisme, de la conduction et de la contractilité cardiaques.
L’association d’antiarythmiques de classes différentes peut apporter un effet thérapeutique bénéfique, mais s’avère le plus souvent très délicate, nécessitant une
surveillance clinique étroite et un contrôle de l’ECG. L’association d’antiarythmiques donnant des torsades de pointes (amiodarone, disopyramide, quinidiniques,
sotalol…) est contre-indiquée.
L’association d’antiarythmiques de même classe est déconseillée, sauf cas exceptionnel, en raison du risque accru d’effets indésirables cardiaques.
L’association à des médicaments ayant des propriétés inotropes négatives, bradycardisantes et/ou ralentissant la conduction auriculo-ventriculaire est délicate et
nécessite une surveillance clinique et un contrôle de l’ECG.
(amiodarone, cibenzoline, diltiazem, disopyramide, dronedarone, flecainide, hydroquinidine, lidocaine, mexiletine, propafenone, quinidine, sotalol, verapamil)
+ AUTRES ANTIARYTHMIQUES
CI - ASDEC - APECL'association de deux antiarythmiques est très délicate. Elle est
dans la majorité des cas, contre-indiquée ou déconseillée.
ANTIARYTHMIQUES CLASSE IA
(disopyramide, hydroquinidine, quinidine)
+ ESMOLOL
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique, ECG et contrôle des concentrations plasmatiques
; si besoin, adaptation de la posologie de l'antiarythmique pendant le
traitement par l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de
l'antiarythmique, par augmentation de son métabolisme hépatique
par l'inducteur.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement de la concentration
plasmatique de l'antiarythmique. Si besoin, adaptation de la posologie
de l'antiarythmique pendant le traitement par la rifampicine et après son
arrêt (risque de surdosage en antiarythmique).
Diminution des concentrations plasmatiques et de l'efficacité de
l'antiarythmique (augmentation de son métabolisme hépatique).
ANTICHOLINESTÉRASIQUES
(voir aussi "bradycardisants")
+ MEDICAMENTS ATROPINIQUES
Il convient de prendre en compte le risque lié à l'association d'un médicament à action atropinique (imipraminiques, neuroleptiques phénothiaziniques,
antispasmodiques, certains antihistaminiques H1…) chez un patient traité par anticholinestérasique. Outre la possible diminution de l'effet thérapeutique de ce dernier,
l'interruption brutale du traitement atropinique expose au risque de dévoiler alors les effets muscariniques du parasympathomimétique avec symptomatologie de type «
crise cholinergique », pouvant se manifester notamment par des convulsions.
+ AUTRES MEDICAMENTS ANTICHOLINESTERASIQUES
Il convient de prendre en compte l'association d'un médicament anticholinestérasique, donné dans une indication telle que la myasthénie ou l'atonie intestinale, à un
autre anticholinestérasique donné dans la maladie d'Alzheimer, en raison d'un risque d'addition des effets indésirables de type cholinergique, notamment digestifs.
(ambenonium, donepezil, galantamine, neostigmine, pyridostigmine, rivastigmine)
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Précaution d'emploi
Surveillance clinique régulière, notamment en début d'association.
Risque de bradycardie excessive (addition des effets
bradycardisants).
+ MÉDICAMENTS ATROPINIQUES
A prendre en compteRisque de moindre efficacité de l’anticholinestérasique par
antagonisme des récepteurs de l’acétylcholine par l’atropinique.
+ PILOCARPINE
A prendre en compteRisque d'addition des effets indésirables cholinergiques,
notamment digestifs.
+ SUXAMETHONIUM
A prendre en compteRisque d'allongement du bloc moteur, majoré en cas de déficit
partiel en pseudocholinestérase.
ANTICOAGULANTS ORAUX
(acenocoumarol, apixaban, dabigatran, édoxaban, fluindione, phenindione, rivaroxaban, warfarine)
+ AUTRES ANTICOAGULANTS ORAUX
A prendre en compte
Tenir compte de la demi-vie de l'anticoagulant oral et observer, le cas
échéant, un délai de carence avant le début du traitement par l'autre.
Penser à informer le patient.
Risque de majoration des événements hémorragiques lors du
relais d'un anticoagulant oral par un autre.
20
+ ACIDE ACETYLSALICYLIQUE
CI - ASDEC - APEC
Contre-indication avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour) et en cas d’antécédent d’ulcère gastro-duodénal
Association déconseillée avec :
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour) en l'absence d’antécédent d’ulcère gastro-duodénal
- des doses antiagrégantes (de 50 mg à 375 mg par jour) et en cas
d’antécédent d’ulcère gastro-duodénal. Nécessité d'un contrôle le cas
échéant, en particulier du temps de saignement.
A prendre en compte avec :
- des doses antiagrégantes (de 50 mg à 375 mg par jour)
Majoration du risque hémorragique, notamment en cas
d’antécédent d’ulcère gastro-duodénal.
+ ANTIAGRÉGANTS PLAQUETTAIRES
A prendre en compteAugmentation du risque hémorragique.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite, voire
biologique .
Augmentation du risque hémorragique de l'anticoagulant oral
(agression de la muqueuse gastroduodénale par les anti-
inflammatoires non stéroïdiens).
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique et le cas échéant, contrôle plus fréquent de l'INR.
Augmentation du risque hémorragique.
+ DÉFIBROTIDE
Association DECONSEILLEERisque hémorragique accru.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
Précaution d'emploi
Lorsque l'association est justifiée, renforcer la surveillance : le cas
échéant, avec les antivitamines K, contrôle biologique au 8e jour, puis
tous les 15 jours pendant la corticothérapie et après son arrêt.
Glucocorticoïdes (voies générale et rectale) : impact éventuel de la
corticothérapie sur le métabolisme de l'antivitamine K et sur celui
des facteurs de la coagulation. Risque hémorragique propre à la
corticothérapie (muqueuse digestive, fragilité vasculaire) à fortes
doses ou en traitement prolongé supérieur à 10 jours.
+ HÉPARINES
CI - PE
Les anticoagulants oraux d'action directe ne doivent pas être
administrés conjointement à l'héparine. Lors du relais de l'un par l'autre,
respecter l'intervalle entre les prises.
Lors du relais héparine/antivitamine K (nécessitant plusieurs jours),
renforcer la surveillance clinique et biologique.
Augmentation du risque hémorragique.
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite (pour les antivitamines K, contrôle plus fréquent de l’INR).
Augmentation du risque hémorragique.
+ IMATINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite (pour les antivitamines K, contrôle plus fréquent de l’INR).
Augmentation du risque hémorragique.
Pour l’apixaban et le rivaroxaban, risque de diminution de leur
métabolisme par l’imatinib, se surajoutant au risque
pharmacodynamique.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteAugmentation du risque hémorragique.
+ IPILIMUMAB
Précaution d'emploi
Surveillance clinique étroite.
Augmentation du risque d'hémorragies digestives.
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
A prendre en compteAugmentation du risque hémorragique.
21
+ THROMBOLYTIQUES
A prendre en compteAugmentation du risque hémorragique.
+ TRAMADOL
A prendre en compte
Surveillance particulièrement chez le sujet âgé.
Augmentation du risque hémorragique
ANTICONVULSIVANTS MÉTABOLISÉS
(acide valproique, ethosuximide, felbamate, fosphenytoine, lamotrigine, oxcarbazepine, pérampanel, phenobarbital, phenytoine, primidone, retigabine, tiagabine,
topiramate, valpromide, zonisamide)
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques et de
l'efficacité de l'anticonvulsivant.
ANTICORPS MONOCLONAUX (HORS ANTI-TNF ALPHA)
(alemtuzumab, amivantamab, anifrolumab, atezolizumab, bélimumab, bimékizumab, blinatumomab, brentuximab, canakinumab, cétuximab, daratumumab,
dénosumab, durvalumab, guselkumab, ibritumomab, inébilizumab, inotuzumab, ipilimumab, ixékizumab, natalizumab, nivolumab, obinutuzumab, ocrélizumab,
ofatumumab, panitumumab, pembrolizumab, ramucirumab, rituximab, satralizumab, sécukinumab, siltuximab, spésolimab, tafasitamab, tézépelumab, tocilizumab,
tralokinumab, ustékinumab, védolizumab)
+ VACCINS VIVANTS ATTÉNUÉS
ASDEC - APEC
Association déconseillée avec :
- anifrolumab, atézolizumab, bélimumab, bimékizumab, blinatumomab,
canakinumab, durvalumab, guselkumab, inébilizumab, inotuzumab,
ixékizumab, obinutuzumab, ocrélizumab, ofatumumab, rituximab,
sacituzumab, spésolimab, tafasitamab, tézépelumab, tocilizumab,
ustékinumab
A prendre en compte avec :
- alemtuzumab, amivantamab, brentuximab, cetuximab, daratumumab,
dénosumab, ibritumomab, ipilimumab, natalizumab, nivolumab,
panitumumab, pembrolizumab, ramucirumab, satralizumab,
sécukinumab, siltuximab, tralokinumab, védolizumab
Risque de maladie vaccinale généralisée, éventuellement mortelle.
ANTIDÉPRESSEURS IMIPRAMINIQUES
(amitriptyline, amoxapine, clomipramine, dosulepine, doxepine, imipramine, maprotiline, trimipramine)
+ ADRÉNALINE (VOIE BUCCO-DENTAIRE OU SOUS-CUTANÉE)
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ ANTIHYPERTENSEURS CENTRAUX
Association DECONSEILLEERisque d'inhibition de l'effet antihypertenseur par l'antidépresseur
(antagonisme au niveau des récepteurs adrénergiques).
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
A prendre en compteEffet vasodilatateur et risque d'hypotension, notamment
orthostatique (effet additif).
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
Précaution d'emploi
Surveillance clinique accrue et, si nécessaire, adaptation posologique.
Augmentation des concentrations plasmatiques de l'antidépresseur
imipraminique avec risque de convulsions et augmentation des
effets indésirables.
+ ORLISTAT
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ SYMPATHOMIMÉTIQUES ALPHA ET BÊTA (VOIE IM ET IV)
Association DECONSEILLEEHypertension paroxystique avec possibilité de troubles du rythme
(inhibition de l'entrée du sympathomimétique dans la fibre
sympathique).
22
ANTIHYPERTENSEURS ALPHA-BLOQUANTS
(doxazosine, prazosine, urapidil)
+ ALPHABLOQUANTS À VISÉE UROLOGIQUE
Association DECONSEILLEEMajoration de l'effet hypotenseur. Risque d'hypotension
orthostatique sévère.
+ ANTIHYPERTENSEURS SAUF ALPHA-BLOQUANTS
A prendre en compteMajoration de l'effet hypotenseur. Risque majoré d'hypotension
orthostatique.
+ INHIBITEURS DE LA PHOSPHODIESTERASE DE TYPE 5
ASDEC - PE
Association déconseillée :
- avec la doxazosine
Précaution d'emploi :
- avec les autres alpha-bloquants
Débuter le traitement aux posologies minimales recommandées et
adapter progressivement les doses si besoin.
Risque d’hypotension orthostatique, notamment chez le sujet âgé.
ANTIHYPERTENSEURS CENTRAUX
(clonidine, guanfacine, methyldopa, moxonidine, rilmenidine)
+ ANTIDÉPRESSEURS IMIPRAMINIQUES
Association DECONSEILLEERisque d'inhibition de l'effet antihypertenseur par l'antidépresseur
(antagonisme au niveau des récepteurs adrénergiques).
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Eviter l'arrêt brutal du traitement par l'antihypertenseur central.
Surveillance clinique.
Augmentation importante de la pression artérielle en cas d'arrêt
brutal du traitement par l'antihypertenseur central.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Association DECONSEILLEEDiminution centrale du tonus sympathique et effet vasodilatateur
des antihypertenseurs centraux, préjudiciables en cas
d'insuffisance cardiaque traitée par bêta-bloquant et vasodilatateur.
+ DILTIAZEM
A prendre en compteTroubles de l'automatisme (troubles de la conduction auriculo-
ventriculaire par addition des effets négatifs sur la conduction).
+ VERAPAMIL
A prendre en compteTroubles de l'automatisme (troubles de la conduction auriculo-
ventriculaire par addition des effets négatifs sur la conduction).
+ YOHIMBINE
Association DECONSEILLEEInhibition possible de l'activité antihypertensive par antagonisme au
niveau des récepteurs.
ANTIHYPERTENSEURS SAUF ALPHA-BLOQUANTS
(acebutolol, altizide, amiloride, amlodipine, atenolol, azilsartan, benazepril, bendroflumethiazide, betaxolol, bisoprolol, bumetanide, candesartan cilexetil, canrenoate de
potassium, captopril, carteolol, celiprolol, chlortalidone, cicletanine, cilazapril, clévidipine, clonidine, clopamide, dihydralazine, diltiazem, enalapril, eplerenone,
eprosartan, felodipine, fosinopril, furosemide, hydrochlorothiazide, indapamide, irbesartan, isradipine, labetalol, lacidipine, lercanidipine, levobunolol, lisinopril, losartan,
manidipine, methyclothiazide, methyldopa, metoprolol, moexipril, moxonidine, nadolol, nebivolol, nicardipine, nifedipine, nimodipine, nitrendipine, olmesartan,
périndopril, pindolol, piretanide, propranolol, quinapril, ramipril, rilmenidine, sotalol, spironolactone, telmisartan, tertatolol, timolol, trandolapril, triamterene, valsartan,
verapamil, zofenopril)
+ ALPHABLOQUANTS À VISÉE UROLOGIQUE
A prendre en compteMajoration de l'effet hypotenseur. Risque d'hypotension
orthostatique majoré.
+ ANTIHYPERTENSEURS ALPHA-BLOQUANTS
A prendre en compteMajoration de l'effet hypotenseur. Risque majoré d'hypotension
orthostatique.
23
ANTI-INFLAMMATOIRES NON STÉROÏDIENS
(aceclofenac, acide mefenamique, acide niflumique, acide tiaprofenique, alminoprofene, celecoxib, dexketoprofene trometamol, diclofenac, etodolac, étoricoxib,
fenoprofene, flurbiprofene, ibuprofene, indometacine, ketoprofene, meloxicam, morniflumate, nabumetone, naproxene, nimesulide, parecoxib, piroxicam, rofecoxib,
sulindac, tenoxicam)
+ AUTRES ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Association DECONSEILLEEAvec les autres anti-inflammatoires non stéroïdiens : majoration du
risque ulcérogène et hémorragique digestif.
+ ACIDE ACETYLSALICYLIQUE
ASDEC - APEC
Association déconseillée avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour)
A prendre en compte avec :
- des doses antiagrégantes (de 50 mg à 375 mg par jour en 1 ou
plusieurs prises)
Majoration du risque ulcérogène et hémorragique digestif.
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Insuffisance rénale aiguë chez le patient à risque (sujet âgé,
déshydratation, traitement associé avec diurétiques, altération de la
fonction rénale), par diminution de la filtration glomérulaire
secondaire à une diminution de la synthèse des prostaglandines
rénales. Ces effets sont généralement réversibles. Par ailleurs,
réduction de l’effet antihypertenseur.
+ ANTIAGRÉGANTS PLAQUETTAIRES
A prendre en compteAugmentation du risque hémorragique, notamment gastro-intestinal.
+ ANTICOAGULANTS ORAUX
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite, voire
biologique .
Augmentation du risque hémorragique de l'anticoagulant oral
(agression de la muqueuse gastroduodénale par les anti-
inflammatoires non stéroïdiens).
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
A prendre en compteRéduction de l'effet antihypertenseur (inhibition des prostaglandines
vasodilatatrices par les anti-inflammatoires non stéroïdiens).
+ CICLOSPORINE
Précaution d'emploi
Surveiller la fonction rénale en début de traitement par l’AINS.
Risque d’addition des effets néphrotoxiques, notamment chez le
sujet âgé.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ DEFERASIROX
A prendre en compteMajoration du risque ulcérogène et hémorragique digestif.
+ DIURÉTIQUES
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l'association.
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Ces effets sont
généralement réversibles. Par ailleurs, réduction de l’effet
antihypertenseur.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
A prendre en compteAugmentation du risque d’ulcération et d’hémorragie gastro-
intestinale.
+ HÉPARINES (DOSES CURATIVES ET/OU SUJET ÂGÉ)
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite.
Augmentation du risque hémorragique (agression de la muqueuse
gastroduodénale par les anti-inflammatoires non stéroïdiens).
24
+ HÉPARINES (DOSES PRÉVENTIVES)
A prendre en compteAugmentation du risque hémorragique.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Ces effets sont
généralement réversibles. Par ailleurs, réduction de l’effet
antihypertenseur.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteMajoration du risque hémorragique.
+ LITHIUM
Association DECONSEILLEE
Si l'association ne peut être évitée, surveiller étroitement la lithémie et
adapter la posologie du lithium pendant l'association et après l'arrêt de
l'anti-inflammatoire non stéroïdien.
Augmentation de la lithémie pouvant atteindre des valeurs toxiques
(diminution de l'excrétion rénale du lithium).
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
A prendre en compteAugmentation du risque hémorragique.
+ METHOTREXATE
ASDEC - PE
Association déconseillée:
- pour des doses de méthotrexate supérieures à 20 mg par semaine.
- avec le kétoprofène et le méthotrexate à des doses supérieures à 20
mg par semaines, respecter un intervalle d'au moins 12 heures entre
l'arrêt ou le début d'un traitement par kétoprofène et la prise de
méthotrexate.
Association nécessitant une précaution d'emploi :
- avec le méthotrexate utilisé à faibles doses (inférieures ou égales à 20
mg par semaine), contrôle hebdomadaire de l'hémogramme durant les
premières semaines de l'association. Surveillance accrue en cas
d'altération (même légère) de la fonction rénale, ainsi que chez le sujet
âgé.
Augmentation de la toxicité hématologique du méthotrexate
(diminution de la clairance rénale du méthotrexate par les anti-
inflammatoires).
+ MIFAMURTIDE
CONTRE-INDICATIONAux doses élevées d’AINS, risque de moindre efficacité du
mifamurtide.
+ NICORANDIL
Association DECONSEILLEEMajoration du risque ulcérogène et hémorragique digestif.
+ PEMETREXED
ASDEC - PE
Association déconseillée :
- en cas de fonction rénale faible à modérée.
Précaution d'emploi :
- en cas de fonction rénale normale. Surveillance biologique de la
fonction rénale.
Risque de majoration de la toxicité du pemetrexed (diminution de
sa clairance rénale par les AINS).
+ TACROLIMUS
Précaution d'emploi
Surveiller la fonction rénale en début de traitement par l’AINS.
Risque d’addition des effets néphrotoxiques, notamment chez le
sujet âgé.
+ TENOFOVIR DISOPROXIL
Précaution d'emploi
En cas d’association, surveiller la fonction rénale.
Risque de majoration de la néphrotoxicité du ténofovir, notamment
avec des doses élevées de l'anti-inflammatoire ou en présence de
facteurs de risque d'insuffisance rénale.
25
ANTIPARASITAIRES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
(chloroquine, halofantrine, lumefantrine, pentamidine, pipéraquine)
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication:
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine
et la pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si cela est possible, interrompre l'un des deux traitements. Si
l'association ne peut être évitée, contrôle préalable du QT et
surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
ANTIPARKINSONIENS ANTICHOLINERGIQUES
(biperidene, trihexyphenidyle, tropatepine)
+ ALCALOÏDES DE L'ERGOT DE SEIGLE DOPAMINERGIQUES
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de majoration des troubles neuropsychiques.
ANTIPARKINSONIENS DOPAMINERGIQUES
(amantadine, apomorphine, bromocriptine, entacapone, lisuride, piribedil, pramipexole, rasagiline, ropinirole, rotigotine, selegiline, tolcapone)
+ NEUROLEPTIQUES ANTIPSYCHOTIQUES (SAUF CLOZAPINE)
Association DECONSEILLEEAntagonisme réciproque du dopaminergique et des neuroleptiques.
Le dopaminergique peut provoquer ou aggraver les troubles
psychotiques. En cas de nécessité d'un traitement par
neuroleptiques chez le patient parkinsonien traité par
dopaminergique, ces derniers doivent être diminués
progressivement jusqu'à l'arrêt (leur arrêt brutal expose à un risque
de "syndrome malin des neuroleptiques").
ANTIPURINES
(azathioprine, mercaptopurine)
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K à la mise en route du traitement par
l'immunomodulateur et après son arrêt.
Augmentation du risque hémorragique.
+ DÉRIVÉS DE L'ACIDE AMINOSALICYLIQUE (ASA)
A prendre en compteRisque de majoration de l'effet myélosuppresseur de
l'immunomodulateur par inhibition de son métabolisme hépatique
par le dérivé de l'ASA, notamment chez les sujets présentant un
déficit partiel en thiopurine méthyltransférase (TPMT).
+ INHIBITEURS DE LA XANTHINE OXYDASE
CONTRE-INDICATIONInsuffisance médullaire éventuellement grave.
+ RIBAVIRINE
Association DECONSEILLEERisque majoré d'effets indésirables graves, par inhibition du
métabolisme de l'immunomodulateur par la ribavirine.
ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
(cimetidine, famotidine, nizatidine, ranitidine)
+ ATAZANAVIR
A prendre en compteRisque de diminution des concentrations plasmatiques de
l'atazanavir.
+ CYANOCOBALAMINE
A prendre en compteRisque de carence en cyanocobalamine après traitement prolongé
(quelques années), la réduction de l’acidité gastrique par ces
médicaments pouvant diminuer l’absorption digestive de la
vitamine B12.
+ INHIBITEURS DE TYROSINE KINASES MÉTABOLISÉS
A prendre en compte
- sauf avec l'entrectinib et le vandétanib.
Risque de diminution de la biodisponibilité de l’inhibiteur de tyrosine
kinases, en raison de son absorption pH-dépendante.
+ ITRACONAZOLE
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ KETOCONAZOLE
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ POSACONAZOLE
Association DECONSEILLEE
Association déconseillée:
- uniquement avec la forme suspension buvable de posaconazole.
Diminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ RILPIVIRINE
A prendre en compte
Si nécessaire, utiliser un antihistaminique H2 actif en une prise par jour,
à prendre au moins 12 heures avant, ou au moins 4 heures après.
Risque de diminution des concentrations plasmatiques de la
rilpivirine.
+ SOTORASIB
A prendre en compteRisque de diminution de l’effet du sotorasib, par diminution de son
absorption.
+ ULIPRISTAL
A prendre en compteRisque de diminution de l’effet de l’ulipristal, par diminution de son
absorption.
ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
(esomeprazole, lansoprazole, omeprazole, pantoprazole, rabeprazole)
+ ATAZANAVIR
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
l'atazanavir, avec risque d'échec thérapeutique.
+ CYANOCOBALAMINE
A prendre en compteRisque de carence en cyanocobalamine après traitement prolongé
(quelques années), la réduction de l’acidité gastrique par ces
médicaments pouvant diminuer l’absorption digestive de la
vitamine B12.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Contrôle clinique et biologique régulier, avec augmentation éventuelle
de la posologie des hormones thyroïdiennes.
Diminution probable de l'absorption des hormones thyroïdiennes,
par augmentation du pH intra-gastrique par l'antisécrétoire.
+ INHIBITEURS DE TYROSINE KINASES MÉTABOLISÉS
A prendre en compte
- sauf avec l'entrectinib, le fédratinib, l'imatinib, le tucatinib et le
vandétanib
Risque de diminution de la biodisponibilité de l’inhibiteur de tyrosine
kinases, en raison de son absorption pH-dépendante.
+ ITRACONAZOLE
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ KETOCONAZOLE
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ LÉDIPASVIR
Précaution d'emploi
Il est recommandé de prendre l'’inhibiteur de la pompe à protons et le
lédipasvir simultanément.
Diminution des concentrations du lédipasvir en cas d’administration
de l’inhibiteur de la pompe à protons avant le lédipasvir.
+ METHOTREXATE
ASDEC - APEC
Association déconseillée :
- avec le méthotrexate aux doses > 20 mg / semaine
A prendre en compte :
- pour des doses inférieures
Risque d’augmentation de la toxicité du méthotrexate par
diminution de son élimination.
27
+ MILLEPERTUIS
A prendre en compteRisque d’inefficacité du traitement antisécrétoire par augmentation
de son métabolisme par le millepertuis.
+ MYCOPHENOLATE MOFETIL
A prendre en compteDiminution des concentrations de l’acide mycophénolique d’environ
un tiers, avec risque potentiel de baisse d’efficacité.
+ POSACONAZOLE
Association DECONSEILLEE
Association déconseillée:
- uniquement avec la forme suspension buvable de posaconazole.
Diminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ RILPIVIRINE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de rilpivirine par
l’inhibiteur de la pompe à protons (absorption diminuée en raison
de l’augmentation du pH gastrique).
+ SOTORASIB
A prendre en compteRisque de diminution de l’effet du sotorasib, par diminution de son
absorption.
+ ULIPRISTAL
A prendre en compteRisque de diminution de l’effet de l’ulipristal, par diminution de son
absorption.
+ VELPATASVIR
Association DECONSEILLEE
Si l’association s’avère nécessaire, la bithérapie velpatasvir/sofosbuvir
doit être prise au moment du repas, ou 4 heures avant la prise d’un IPP
donné à dose minimale.
Diminution des concentrations de velpatasvir et de sofosbuvir.
ANTISEPTIQUES MERCURIELS
(merbromine, thiomersal)
+ POVIDONE IODÉE
Association DECONSEILLEEErythèmes, phlyctènes, voire nécrose cutanéo-muqueuse
(formation d'un complexe caustique en cas d'utilisation
concomitante d'antiseptiques iodés et mercuriels). L'interaction
dépend de la stabilité de l'organo-mercuriel au niveau cutané et de
la sensibilité individuelle.
ANTISPASMODIQUES URINAIRES
(darifenacine, fesoterodine, oxybutynine, solifenacine, tolterodine)
+ INHIBITEURS PUISSANTS DU CYP3A4
CI - ASDEC - PE
Contre-indication :
- avec la darifénacine
- avec la fésotérodine et la solifénacine, en cas d'insuffisance rénale ou
hépatique, modérée à sévère.
Association déconseillée :
- avec la toltérodine
Précaution d'emploi:
- avec la fésotérodine ou la solifénacine, chez le patient à fonction
rénale et hépatique normales, réduire la dose à 4 mg ou 5 mg,
respectivement, en cas d'association à un inhibiteur puissant du
CYP3A4.
A prendre en compte :
- avec l'oxybutynine.
Risque de majoration des effets indésirables.
ANTI-TNF ALPHA
(adalimumab, certolizumab, etanercept, golimumab, infliximab)
+ ABATACEPT
Association DECONSEILLEEMajoration de l’immunodépression.
28
+ ANAKINRA
Association DECONSEILLEERisque accru d'infections graves et de neutropénies.
+ CANAKINUMAB
Association DECONSEILLEERisque de majoration des infections graves.
+ VACCINS VIVANTS ATTÉNUÉS
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
ANTITUSSIFS MORPHINE-LIKE
(dextromethorphane, noscapine, pholcodine)
+ ANALGÉSIQUES MORPHINIQUES AGONISTES
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ METHADONE
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
ANTITUSSIFS MORPHINIQUES VRAIS
(codeine, ethylmorphine)
+ ANALGÉSIQUES MORPHINIQUES AGONISTES
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ METHADONE
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ MORPHINIQUES AGONISTES-ANTAGONISTES
Association DECONSEILLEEDiminution de l'effet antalgique ou antitussif du morphinique, par
blocage compétitif des récepteurs, avec risque d'apparition d'un
syndrome de sevrage.
ANTIVITAMINES K
ANTI-INFECTIEUX ET HEMOSTASE
De nombreux cas d’augmentation de l’activité des antivitamines K ont été rapportés chez des patients recevant des antibiotiques. Le contexte infectieux ou
inflammatoire marqué, l’âge et l’état général du patient apparaissent comme des facteurs de risque. Dans ces circonstances, il apparaît difficile de faire la part entre la
pathologie infectieuse et son traitement dans la survenue du déséquilibre de l’INR. Cependant, certaines classes d’antibiotiques sont davantage impliquées : il s’agit
notamment des fluoroquinolones, des macrolides, des cyclines, du cotrimoxazole et de certaines céphalosporines, qui imposent, dans ces conditions, de renforcer la
surveillance de l'INR. Certaines céphalosporines (céfamandole, ceftriaxone, céfazoline), la clindamycine, semblent interagir au niveau de l’hémostase avec apparition
d’anticorps anti facteur V. Enfin, la tigécycline et le danazol possèdent une action fibrinolytique propre.
AVK et INR
Chez un patient traité par antivitamines K, il convient de contrôler l’INR à chaque initiation ou suppression d’un ou plusieurs médicaments. La modification soudaine
des habitudes alimentaires doit être également prise en compte et la régularité est préconisée pour le maintien à l’équilibre de l’INR. Les aliments riches en vitamine K
sont essentiellement représentés par les choux, épinards, brocolis, certaines salades.
(acenocoumarol, fluindione, warfarine)
+ ALLOPURINOL
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'allopurinol et 8 jours après
son arrêt.
Augmentation du risque hémorragique.
+ AMIODARONE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'amiodarone et jusqu'à 4
semaines après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ ANDROGÈNES
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation de la posologie de
l’antivitamine K pendant le traitement par l'androgène et après son arrêt.
Augmentation du risque hémorragique par effet direct sur la
coagulation et/ou les systèmes fibrinolytiques.
29
+ ANTIPURINES
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K à la mise en route du traitement par
l'immunomodulateur et après son arrêt.
Augmentation du risque hémorragique.
+ APREPITANT
A prendre en compteRisque de diminution de l’effet de l’antivitamine K par augmentation
de son métabolisme hépatique par l’aprépitant.
+ BOSENTAN
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique.
+ CEFAMANDOLE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la céphalosporine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ CEFAZOLINE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la céphalosporine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ CEFTRIAXONE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la céphalosporine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ CIMETIDINE
A prendre en compteAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de l'effet de l'antivitamine K et du risque
hémorragique (diminution de son métabolisme hépatique).
+ CLINDAMYCINE
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par clindamycine et après son
arrêt.
Augmentation de l’effet de l’antivitamine K et du risque
hémorragique.
+ COLCHICINE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la colchicine et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ CYCLINES
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la cycline et après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique (pour la tigécycline, effet direct sur la coagulation
et/ou les systèmes fibrinolytiques).
+ CYTOTOXIQUES
Précaution d'emploi
Contrôle plus fréquent de l'INR.
Augmentation du risque thrombotique et hémorragique au cours
des affections tumorales. De surcroit, possible interaction entre les
AVK et la chimiothérapie.
+ DANAZOL
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation de la posologie de
l’antivitamine K pendant le traitement par le danazol et après son arrêt.
Augmentation du risque hémorragique par effet direct sur la
coagulation et/ou les systèmes fibrinolytiques.
+ DEFERASIROX
A prendre en compteMajoration du risque ulcérogène et hémorragique digestif.
+ DISULFIRAME
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation de la posologie de
l'antivitamine K pendant le traitement par le disulfirame et 8 jours après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
30
+ ECONAZOLE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par éconazole et après son
arrêt.
Quelle que soit la voie d'administration de l'éconazole :
augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ EFAVIRENZ
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique.
+ FIBRATES
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par le fibrate et 8 jours après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ FLUCONAZOLE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par le fluconazole et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ FLUOROQUINOLONES
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la fluoroquinolone et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ FLUOROURACILE (ET, PAR EXTRAPOLATION, AUTRES FLUOROPYRIMIDINES)
Association DECONSEILLEE
Si elle ne peut être évitée, contrôle plus fréquent de l'INR. Adaptation de
la posologie de l'antivitamine K pendant le traitement par le cytotoxique
et 8 jours après son arrêt.
Augmentation importante de l'effet de l'antivitamine K et du risque
hémorragique.
+ GLUCOSAMINE
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adapation éventuelle de la posologie de
l’antivitamine K.
Augmentation du risque hémorragique.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'anticonvulsivant inducteur
et 8 jours après son arrêt.
Diminution (ou, rarement, augmentation avec la phénytoïne) de
l'effet de l'antivitamine K par augmentation de son métabolisme
hépatique par l'anticonvulsivant inducteur.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant la durée du traitement.
Variation de l'effet de l'antivitamine K, le plus souvent dans le sens
d'une diminution.
+ LEVOCARNITINE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la lévocarnitine et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique
+ MACROLIDES (SAUF SPIRAMYCINE)
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par le macrolide et après son
arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ METHYLPREDNISOLONE
Précaution d'emploi
Contrôle de l'INR 2 à 4 jours après le bolus de méthylprednisolone ou
en présence de tous signes hémorragiques.
Pour des doses de 0,5 à 1g de méthylprednisolone administrées en
bolus : augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ MICONAZOLE
CONTRE-INDICATIONHémorragies imprévisibles, éventuellement graves.
31
+ MILLEPERTUIS
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler l'INR avant puis après l'arrêt du millepertuis.
Diminution des concentrations plasmatiques de l'antivitamine K, en
raison de son effet inducteur enzymatique, avec risque de baisse
d'efficacité voire d'annulation de l'effet dont les conséquences
peuvent être éventuellement graves (évènement thrombotique).
+ NEVIRAPINE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique.
+ NOSCAPINE
Association DECONSEILLEEAugmentation de l’effet de l’antivitamine K et du risque
hémorragique.
+ ORLISTAT
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'orlistat et après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ PARACETAMOL
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par le paracétamol et après
son arrêt.
Risque d’augmentation de l’effet de l’antivitamine K et du risque
hémorragique en cas de prise de paracétamol aux doses
maximales (4 g/j) pendant au moins 4 jours.
+ PENTOXIFYLLINE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la pentoxifylline et 8 jours
après son arrêt.
Augmentation du risque hémorragique.
+ PRISTINAMYCINE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la pristinamycine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ PROGUANIL
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par le proguanil et après son
arrêt.
Risque d’augmentation de l’effet de l’antivitamine K et du risque
hémorragique.
+ RIFAMPICINE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la rifampicine et 8 jours
après son arrêt.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique par la rifampicine.
+ ROPINIROLE
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par ropinirole et après son
arrêt.
Augmentation du risque hémorragique.
+ SULFAMETHOXAZOLE
Association DECONSEILLEE
Si l’association ne peut être évitée, contrôle plus fréquent de l’INR et
adaptation de la posologie de l’antivitamine K pendant le traitement par
cotrimoxazole et après son arrêt.
Augmentation importante de l’effet de l’antivitamine K et du risque
hémorragique.
+ TAMOXIFENE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Risque d'augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ TIBOLONE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la tibolone et après son
arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ VORICONAZOLE
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par voriconazole et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique par diminution de son métabolisme hépatique.
32
APALUTAMIDE
Voir aussi : inducteurs enzymatiques - inducteurs enzymatiques puissants - médicaments à l'origine d'un hypogonadisme masculin
+ ATORVASTATINE
Association DECONSEILLEERisque de diminution très importante des concentrations de
l'atorvastatine, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ CABAZITAXEL
Association DECONSEILLEERisque de diminution très importante des concentrations du
cabazitaxel, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ DOCETAXEL
Association DECONSEILLEERisque de diminution très importante des concentrations du
docétaxel, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEERisque de diminution très importante des concentrations des
immunosuppresseurs, et perte d‘efficacité, par augmentation de
leur métabolisme hépatique par l’apalutamide.
+ METHADONE
Association DECONSEILLEERisque de diminution très importante des concentrations de la
méthadone, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ OLAPARIB
Association DECONSEILLEERisque de diminution très importante des concentrations de
l'olaparib, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ OMEPRAZOLE
Association DECONSEILLEERisque de diminution très importante des concentrations de
l'oméprazole, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ PIMOZIDE
Association DECONSEILLEERisque de diminution très importante des concentrations du
pimozide, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ SIMVASTATINE
Association DECONSEILLEERisque de diminution très importante des concentrations de la
simvastatine, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
APIXABAN
Voir aussi : anticoagulants oraux - substrats à risque du CYP3A4
+ FLUCONAZOLE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l'apixaban par le
fluconazole, avec majoration du risque de saignement.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques de l’apixaban par
l'inducteur enzymatique, avec risque de réduction de l’effet
thérapeutique.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l’apixaban par
l'inhibiteur, avec majoration du risque de saignement.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de l’apixaban par la
rifampicine, avec risque de diminution de l’effet thérapeutique.
33
APOMORPHINE
Voir aussi : antiparkinsoniens dopaminergiques - dopaminergiques - médicaments à l'origine d'une hypotension orthostatique
+ SÉTRONS
CONTRE-INDICATIONDes hypotensions sévères et des pertes de connaissance ont été
rapportées lors de l’association d’un sétron avec l’apomorphine.
APRÉMILAST
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations plasmatiques d’aprémilast par
augmentatiion de son métabolisme par l’inducteur.
APREPITANT
+ ANTIVITAMINES K
A prendre en compteRisque de diminution de l’effet de l’antivitamine K par augmentation
de son métabolisme hépatique par l’aprépitant.
+ CYPROTERONE
Précaution d'emploi
Dans son utilisation comme contraceptif hormonal :
Utiliser une méthode de contraception fiable, additionnelle ou
alternative, pendant la durée de l'association.
Risque de diminution des concentrations de la cyprotérone avec
risque de moindre efficacité contraceptive.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de
l’aprépitant.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par l'aprépitant.
+ IFOSFAMIDE
A prendre en compteRisque d’augmentation de la neurotoxicité de l’ifosfamide.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEERisque de diminution très importante des concentrations
d'aprépitant.
+ ITRACONAZOLE
A prendre en compteAugmentation des concentrations d’aprépitant par diminution de
son métabolisme hépatique par l’itraconazole.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ PROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique, pendant la durée de l'association et un cycle
suivant.
(Sauf stérilet), diminution des concentrations du progestatif, avec
risque de moindre efficacité contraceptive.
+ RIFAMPICINE
Association DECONSEILLEEDiminution très importante des concentrations d'aprépitant.
ARIPIPRAZOLE
Voir aussi : médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - neuroleptiques - neuroleptiques antipsychotiques (sauf clozapine)
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
l’aripiprazole pendant l’association et 1 à 2 semaines après l’arrêt de
l’inducteur.
Diminution des concentrations plasmatiques de l’aripiprazole.
+ NEUROLEPTIQUES ANTIPSYCHOTIQUES (SAUF CLOZAPINE)
A prendre en compteRisque de moindre efficacité, notamment de l’aripiprazole, suite à
l’antagonisme des récepteurs dopaminergiques par le
neuroleptique.
34
ARSENIEUX
Voir aussi : substances susceptibles de donner des torsades de pointes
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
ATALUREN
+ AMINOSIDES
CONTRE-INDICATIONRisque de potentialisation de la toxicité rénale de l’aminoside.
ATAZANAVIR
Voir aussi : inhibiteurs de protéases boostés par ritonavir
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compteRisque de diminution des concentrations plasmatiques de
l'atazanavir.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
l'atazanavir, avec risque d'échec thérapeutique.
+ BICTÉGRAVIR
Association DECONSEILLEEQuadruplement des concentrations de bictégravir.
+ BUPRENORPHINE
A prendre en compteRisque de majoration ou de diminution des effets de la
buprénorphine, à la fois par inhibition et accélération de son
métabolisme par l’inhibiteur de protéases.
+ CLARITHROMYCINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Augmentation des concentrations plasmatiques de clarithromycine
et inhibition de la formation de son métabolite actif.
+ EFAVIRENZ
Association DECONSEILLEE
Si l’association s’avère nécessaire, adaptation posologique de
l’atazanavir avec surveillance clinique et biologique régulière,
notamment en début d’association.
Risque de baisse de l’efficacité de l’atazanavir par augmentation de
son métabolisme hépatique.
+ ETRAVIRINE
Association DECONSEILLEERisque de diminution des concentrations plasmatiques d’atazanavir
par l’étravirine.
+ GLÉCAPRÉVIR + PIBRENTASVIR
CONTRE-INDICATIONAugmentation de l’hépatotoxicité avec la bithérapie.
+ LÉNACAPAVIR
Association DECONSEILLEELorsqu’il est associé au cobicistat, l’atazanavir provoque une
augmentation très importante des concentrations de lénacapavir.
+ NEVIRAPINE
Association DECONSEILLEE
Si l’association s’avère nécessaire, adaptation posologique de
l’atazanavir avec surveillance clinique et biologique régulière,
notamment en début d’association.
Risque de baisse de l’efficacité de l’atazanavir par augmentation de
son métabolisme hépatique.
35
+ POSACONAZOLE
A prendre en compteAugmentation des concentrations plasmatiques de l'atazanavir et
du risque d'hyperbilirubinémie.
+ TENOFOVIR DISOPROXIL
A prendre en compte
Ne pas administrer l’atazanavir avec le ténofovir sans ritonavir.
Diminution d’environ un tiers de l’exposition à l’atazanavir chez le
patient en cas d’association au ténofovir, comparativement au sujet
sain recevant la même association.
ATORVASTATINE
Voir aussi : inhibiteurs de l'HMG-CoA réductase (statines) - médicaments à l'origine d'atteintes musculaires - substrats à risque du CYP3A4
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations de
l'atorvastatine, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ AZITHROMYCINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ CICLOSPORINE
Précaution d'emploi
Ne pas dépasser la posologie de 10mg/jour d'atorvastatine. Si l'objectif
thérapeutique n'est pas atteint à cette posologie, utiliser une autre
statine non concernée par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme de
l'hypocholestérolémiant).
+ CLARITHROMYCINE
Précaution d'emploi
Utiliser des doses plus faibles d'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholesterolémiant.
+ DILTIAZEM
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ ERYTHROMYCINE
Précaution d'emploi
Utiliser des doses plus faibles d'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholesterolémiant.
+ FLUCONAZOLE
Précaution d'emploi
Utiliser des doses plus faibles de l'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables concentration-dépendants à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
statine).
+ GLÉCAPRÉVIR + PIBRENTASVIR
CONTRE-INDICATIONAugmentation importante des concentrations plasmatiques
d’atorvastatine par la bithérapie, avec risque majoré d’effets
indésirables (concentration-dépendants) à type de rhabdomyolyses.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Association DECONSEILLEE
Utiliser des doses plus faibles d'atorvastatine. Si l'objectif thérapeutique
n'est pas atteint, utiliser une autre statine non concernée par ce type
d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l'atorvastatine).
+ ITRACONAZOLE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l'atorvastatine).
+ KETOCONAZOLE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l'atorvastatine).
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'atorvastatine
par diminution de son métabolisme hépatique par la bithérapie.
36
+ PAMPLEMOUSSE (JUS ET FRUIT)
A prendre en compteAugmentation des concentrations plasmatiques de l'hypolipémiant,
avec risque de survenue d'effets indésirables, notamment
musculaires.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de
l'atrovastatine par augmentation de son absorption intestinale par
le ponatinib.
+ POSACONAZOLE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l’inhibiteur de l’HMG-CoA reductase).
+ RANOLAZINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par inhibition du métabolisme de
l'atorvastatine par la ranolazine.
+ RIFAMPICINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques
d'atorvastatine, par augmentation de son métabolisme hépatique
par la rifampicine.
+ ROXITHROMYCINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse.
+ STIRIPENTOL
CONTRE-INDICATIONRisque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
+ TELITHROMYCINE
CONTRE-INDICATIONRisque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
+ VERAPAMIL
Précaution d'emploi
Utiliser des doses plus faibles d'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
ATOVAQUONE
+ EFAVIRENZ
Association DECONSEILLEEDiminution des concentrations plasmatiques d'atovaquone par
l'inducteur enzymatique.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Association DECONSEILLEEDiminution, éventuellement très importante, des concentrations
plasmatiques de l’atovaquone par augmentation de son
métabolisme.
+ RIFABUTINE
A prendre en compteDiminution modérée des concentrations plasmatiques
d'atovaquone par l'inducteur enzymatique.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques d'atovaquone par
l'inducteur enzymatique.
AVANAFIL
Voir aussi : inhibiteurs de la phosphodiesterase de type 5 - médicaments à l'origine d'une hypotension orthostatique
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l'avanafil, avec
risque d’hypotension.
37
AZITHROMYCINE
Voir aussi : macrolides (sauf spiramycine)
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ IVABRADINE
Précaution d'emploi
Surveillance clinique et ECG pendant l’association.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes. De plus, risque d'augmentation des
concentrations plasmatiques de l’ivabradine par augmentation de
son absorption par l’azithromycine.
+ SIMVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
AZTREONAM
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation éventuelle de
la posologie de l'anticonvulsivant pendant le traitement par l'anti-
infectieux et après son arrêt.
Risque de survenue de crises convulsives, par diminution des
concentrations plasmatiques de l'acide valproïque.
BACLOFENE
Voir aussi : médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique
+ LEVODOPA
A prendre en compteRisque d’aggravation du syndrome parkinsonien ou d’effets
indésirables centraux (hallucinations visuelles, état confusionnel,
céphalées).
BARBITURIQUES
(phenobarbital, primidone, thiopental)
+ BENZODIAZÉPINES ET APPARENTÉS
A prendre en compteRisque majoré de sédation et de dépression respiratoire pouvant
entraîner coma et décès, notamment chez le sujet âgé. Il convient
de limiter autant que possible les doses et la durée de l’association.
+ MORPHINIQUES
A prendre en compteRisque majoré de sédation et de dépression respiratoire pouvant
entraîner coma et décès, notamment chez le sujet âgé. Il convient
de limiter autant que possible les doses et la durée de l’association.
+ OXYBATE DE SODIUM
CONTRE-INDICATIONRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
BAZÉDOXIFÈNE
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Surveillance d'éventuels signes évocateurs d’une perte d’efficacité
(saignements).
Diminution des concentrations plasmatiques de bazédoxifène par
l’inducteur.
BÉDAQUILINE
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations plasmatiques de bédaquiline par
augmentation de son métabolisme par l’inducteur.
38
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si l’association est nécessaire, une surveillance ECG plus fréquente et
une surveillance des transaminases sont recommandées.
Augmentation des concentrations plasmatiques de bédaquiline par
diminution de son métabolisme hépatique par l’inhibiteur.
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
bédaquiline par augmentation de son métabolisme par l’inducteur.
BÉLATACEPT
+ VACCINS VIVANTS ATTÉNUÉS
Association DECONSEILLEERisque de maladie vaccinale généralisée, éventuellement mortelle.
BENZODIAZÉPINES ET APPARENTÉS
(alprazolam, avizafone, bromazepam, chlordiazepoxide, clobazam, clonazepam, clorazepate, clotiazepam, diazepam, estazolam, eszopiclone, flunitrazepam,
flurazepam, loflazépate, loprazolam, lorazepam, lormetazepam, midazolam, nitrazepam, nordazepam, oxazepam, prazepam, tetrazepam, zolpidem, zopiclone)
+ BARBITURIQUES
A prendre en compteRisque majoré de sédation et de dépression respiratoire pouvant
entraîner coma et décès, notamment chez le sujet âgé. Il convient
de limiter autant que possible les doses et la durée de l’association.
+ BUPRENORPHINE
A prendre en compte
Evaluer attentivement le rapport bénéfice/risque de cette association.
Informer le patient de la nécessité de respecter les doses prescrites.
Avec la buprénorphine utilisée en traitement de substitution : risque
majoré de dépression respiratoire, pouvant être fatale.
+ CLOZAPINE
A prendre en compteRisque accru de collapsus avec arrêt respiratoire et / ou cardiaque.
+ MORPHINIQUES
A prendre en compteRisque majoré de sédation et de dépression respiratoire pouvant
entraîner coma et décès, notamment chez le sujet âgé. Il convient
de limiter autant que possible les doses et la durée de l’association.
BÊTA-2 MIMÉTIQUES
(bambuterol, indacatérol, olodatérol, salbutamol, terbutaline, vilantérol)
+ BÊTA-BLOQUANTS NON CARDIO-SÉLECTIFS (Y COMPRIS COLLYRES)
A prendre en compteRisque de moindre efficacité réciproque par antagonisme
pharmacodynamique.
+ HALOTHANE
Association DECONSEILLEE
Interrompre le traitement par bêta-2 mimétiques si l'anesthésie doit se
faire sous halothane.
En cas d'intervention obstétricale, majoration de l'inertie utérine
avec risque hémorragique ; par ailleurs, troubles du rythme
ventriculaires graves, par augmentation de la réactivité cardiaque.
+ INSULINE
Précaution d'emploi
Renforcer la surveillance sanguine et urinaire.
Elévation de la glycémie par le bêta-2 mimétique.
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Renforcer la surveillance sanguine et urinaire. Passer éventuellement à
l'insuline, le cas échéant.
Elévation de la glycémie par le bêta-2 mimétique.
BÊTA-BLOQUANTS (SAUF ESMOLOL ET SOTALOL) (Y COMPRIS COLLYRES)
(acebutolol, atenolol, betaxolol, bisoprolol, carteolol, celiprolol, labetalol, levobunolol, metoprolol, nadolol, nebivolol, pindolol, propranolol, tertatolol, timolol)
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de l'automatisme et de la conduction (suppression des
mécanismes sympathiques compensateurs).
39
BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
(acebutolol, atenolol, betaxolol, bisoprolol, carteolol, celiprolol, labetalol, levobunolol, metoprolol, nadolol, nebivolol, pindolol, propranolol, sotalol, tertatolol, timolol)
+ ANESTHÉSIQUES VOLATILS HALOGÉNÉS
Précaution d'emploi
En règle générale, ne pas arrêter le traitement bêta-bloquant et, de
toute façon, éviter l'arrêt brutal. Informer l'anesthésiste de ce traitement.
Réduction des réactions cardiovasculaires de compensation par les
bêta-bloquants. L'inhibition bêta-adrénergique peut être levée
durant l'intervention par les bêta-mimétiques.
+ ANTIHYPERTENSEURS CENTRAUX
Précaution d'emploi
Eviter l'arrêt brutal du traitement par l'antihypertenseur central.
Surveillance clinique.
Augmentation importante de la pression artérielle en cas d'arrêt
brutal du traitement par l'antihypertenseur central.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
A prendre en compteRéduction de l'effet antihypertenseur (inhibition des prostaglandines
vasodilatatrices par les anti-inflammatoires non stéroïdiens).
+ DIHYDROPYRIDINES
A prendre en compteHypotension, défaillance cardiaque chez les patients en
insuffisance cardiaque latente ou non contrôlée (addition des effets
inotropes négatifs). Le bêta-bloquant peut par ailleurs minimiser la
réaction sympathique réflexe mise en jeu en cas de répercussion
hémodynamique excessive.
+ DILTIAZEM
Association DECONSEILLEE
Une telle association ne doit se faire que sous surveillance clinique et
ECG étroite, en particulier chez le sujet âgé ou en début de traitement.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
troubles de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
+ DIPYRIDAMOLE
A prendre en compteAvec le dipyridamole par voie injectable : majoration de l'effet
antihypertenseur.
+ GLINIDES
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêta-bloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ GLIPTINES
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ INSULINE
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ LIDOCAINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations plasmatiques de lidocaïne pendant l'association et après
l'arrêt du bêta-bloquant. Adaptation si besoin de la posologie de la
lidocaïne.
Avec la lidocaïne utilisée par voie IV : augmentation des
concentrations plasmatiques de lidocaïne avec possibilité d'effets
indésirables neurologiques et cardiaques (diminution de la
clairance hépatique de la lidocaïne).
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêta-bloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ VERAPAMIL
Association DECONSEILLEE
Une telle association ne doit se faire que sous surveillance clinique et
ECG étroite, en particulier chez le sujet âgé ou en début de traitement.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
trouble de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
40
BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
A l’heure actuelle, 4 bêta-bloquants ont l'indication "insuffisance cardiaque" : le carvédilol, le bisoprolol, le métoprolol et le névibolol.
Les interactions médicamenteuses des bêta-bloquants, lorsqu’ils sont prescrits dans l’insuffisance cardiaque, peuvent avoir des conséquences cliniques plus sévères
que celles rencontrées lors de leur prescription dans d’autres indications. Ainsi, certaines associations médicamenteuses, couramment réalisées dans les indications
classiques des bêta-bloquants, doivent être reconsidérées à la lumière de cette indication très particulière, avec un niveau de recommandation souvent plus
contraignant.
(bisoprolol, carvedilol, metoprolol, nebivolol)
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et ECG régulière.
Troubles de l'automatisme et de la conduction cardiaque avec
risque de bradycardie excessive.
+ ANESTHÉSIQUES VOLATILS HALOGÉNÉS
Précaution d'emploi
En règle générale, ne pas arrêter le traitement bêta-bloquant et, de
toute façon, éviter l'arrêt brutal. Informer l'anesthésiste de ce traitement.
Réduction des réactions cardiovasculaires de compensation par les
bêta-bloquants. L'inhibition bêta-adrénergique peut être levée
durant l'intervention par les bêta-stimulants.
+ ANTICHOLINESTÉRASIQUES
Précaution d'emploi
Surveillance clinique régulière, notamment en début d'association.
Risque de bradycardie excessive (addition des effets
bradycardisants).
+ ANTIDÉPRESSEURS IMIPRAMINIQUES
A prendre en compteEffet vasodilatateur et risque d'hypotension, notamment
orthostatique (effet additif).
+ ANTIHYPERTENSEURS CENTRAUX
Association DECONSEILLEEDiminution centrale du tonus sympathique et effet vasodilatateur
des antihypertenseurs centraux, préjudiciables en cas
d'insuffisance cardiaque traitée par bêta-bloquant et vasodilatateur.
+ DIGOXINE
A prendre en compteTroubles de l’automatisme (bradycardie, arrêt sinusal) et troubles
de la conduction sino-auriculaire et auriculo-ventriculaire.
+ DIHYDROPYRIDINES
A prendre en compteHypotension, défaillance cardiaque chez les malades en
insuffisance cardiaque latente ou non contrôlée (effet inotrope
négatif in vitro des dihydropyridines plus ou moins marqué et
susceptibles de s'additionner aux effets inotropes négatifs des bêta-
bloquants). La présence d'un traitement bêta-bloquant peut par
ailleurs minimiser la réaction sympathique réflexe mise en jeu en
cas de répercussion hémodynamique excessive.
+ DILTIAZEM
Association DECONSEILLEEEffet inotrope négatif avec risque de décompensation de
l’insuffisance cardiaque, troubles de l'automatisme (bradycardie,
arrêt sinusal) et troubles de la conduction sino-auriculaire et
auriculo-ventriculaire.
+ GLINIDES
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ INSULINE
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ LIDOCAINE
A prendre en compteEffet inotrope négatif avec risque de décompensation cardiaque.
+ MEXILETINE
CONTRE-INDICATIONEffet inotrope négatif avec risque de décompensation cardiaque.
+ NEUROLEPTIQUES
A prendre en compteEffet vasodilatateur et risque d'hypotension, notamment
orthostatique (effet additif).
41
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Prévenir le malade et renforcer, surtout au début du traitement,
l'autosurveillance sanguine.
Tous les bêta-bloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ VERAPAMIL
Association DECONSEILLEEEffet inotrope négatif avec risque de décompensation de
l’insuffisance cardiaque, troubles de l'automatisme (bradycardie,
arrêt sinusal) et troubles de la conduction sino-auriculaire et
auriculo-ventriculaire.
BÊTA-BLOQUANTS NON CARDIO-SÉLECTIFS (Y COMPRIS COLLYRES)
(carteolol, carvedilol, labetalol, nadolol, pindolol, propranolol, sotalol, tertatolol, timolol)
+ BÊTA-2 MIMÉTIQUES
A prendre en compteRisque de moindre efficacité réciproque par antagonisme
pharmacodynamique.
BICTÉGRAVIR
Voir aussi : inhibiteurs d'intégrase - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ATAZANAVIR
Association DECONSEILLEEQuadruplement des concentrations de bictégravir.
+ FER
Précaution d'emploi
Prendre le bictégravir au moins 2 heures avant les sels de fer, ou en
même temps qu’un repas.
Diminution de près des deux tiers de l'absorption du bictégravir en
cas d’ingestion simultanée ou à jeun.
+ INDUCTEURS ENZYMATIQUES
CI - ASDEC
Contre-indication :
- avec la rifampicine
Association déconseillée :
- avec les autres inducteurs enzymatiques
Risque de perte d’efficacité par diminution, éventuellement
importante, des concentrations de bictégravir.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution très importante des concentrations de bictégravir, avec
risque de perte d’efficacité.
+ RIFAMPICINE
CONTRE-INDICATIONDiminution très importante des concentrations de bictégravir, avec
risque de perte d’efficacité.
BISPHOSPHONATES
(acide alendronique, acide clodronique, acide etidronique, acide ibandronique, acide oxidronique, acide pamidronique, acide risedronique, acide tiludronique, acide
zoledronique)
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium et antiacides à distance des
bisphosphonates (de 30 minutes au minimum à plus de 2 heures, si
possible, selon le bisphosphonate).
Pour les sels de calcium administrés par voie orale : diminution de
l'absorption digestive des bisphosphonates.
+ FER
Précaution d'emploi
Prendre les sels de fer à distance des bisphosphonates (de 30 minutes
au minimum à plus de 2 heures, si possible, selon le bisphosphonate).
Pour les sels de fer administrés par voie orale : diminution de
l'absorption digestive des bisphosphonates.
BLEOMYCINE
Voir aussi : cytotoxiques
+ BRENTUXIMAB
CONTRE-INDICATIONRisque de majoration de la toxicité pulmonaire.
42
BORTEZOMIB
Voir aussi : cytotoxiques - substrats à risque du CYP3A4
+ INDUCTEURS ENZYMATIQUES
A prendre en compteDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
bortezomib pendant la durée du traitement par l’inhibiteur enzymatique.
Risque de majoration des effets indésirables, notamment
neurologiques, du bortezomib par diminution de son métabolisme.
BOSENTAN
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique.
+ CICLOSPORINE
CONTRE-INDICATIONDiminution importante des concentrations sanguines de la
ciclosporine et augmentation des concentrations plasmatiques de
bosentan.
+ CYPROTERONE
Précaution d'emploi
Dans ses indications comme anti-androgène, surveillance clinique et si
possible adaptation de la posologie de la cyprotérone pendant
l'administration avec le bosentan et après son arrêt.
Dans son utilisation comme contraceptif hormonal, utiliser une méthode
de contraception fiable, additionnelle ou alternative pendant la durée de
l'association.
Risque de diminution de l'efficacité de la cyprotérone.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du bosentan.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par le bosentan.
+ GLIBENCLAMIDE
Précaution d'emploi
Surveillance de la glycémie, adaptation du traitement si besoin, et
surveillance des constantes biologiques hépatiques.
Risque de moindre efficacité du glibenclamide par diminution de
ses concentrations plasmatiques, en raison de l'effet inducteur du
bosentan. Par ailleurs, des cas d'hépatotoxicité ont été rapportés
lors de l'association.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et biologique pendant l’association.
Risque majoré des effets indésirables du bosentan, notamment
d’atteintes hépatiques, par diminution de son métabolisme par
l'inhibiteur.
+ PROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode contraceptive fiable, additionnelle ou alternative,
pendant la durée de l'association et un cycle suivant.
Risque de diminution de l'efficacité du contraceptif hormonal par
augmentation de son métabolisme hépatique.
+ PROGESTATIFS NON CONTRACEPTIFS, ASSOCIÉS OU NON À UN ESTROGÈNE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant l’administration du bosentan et après son
arrêt.
Risque de diminution de l’efficacité du progestatif.
+ RIFAMPICINE
Association DECONSEILLEERisque de diminution, importante pour la rifampicine, des
concentrations plasmatiques de bosentan.
BOTULIQUE (TOXINE)
+ AMINOSIDES
Association DECONSEILLEE
Utiliser un autre antibiotique.
Risque d'augmentation des effets de la toxine botulique avec les
aminosides (par extrapolation à partir des effets observés au cours
du botulisme).
43
BRADYCARDISANTS
De nombreux médicaments peuvent entraîner une bradycardie. C'est le cas notamment des antiarythmiques de classe Ia, des bêta-bloquants, de certains
antiarythmiques de classe III, de certains antagonistes du calcium, de la digoxine, de la pilocarpine, des anticholinestérasiques… etc.
(acebutolol, ambenonium, amiodarone, atenolol, betaxolol, bisoprolol, carteolol, carvedilol, celiprolol, clonidine, crizotinib, digoxine, diltiazem, disopyramide, donepezil,
dronedarone, esmolol, fampridine, fingolimod, galantamine, hydroquinidine, ivabradine, labetalol, levobunolol, mefloquine, metoprolol, midodrine, nadolol, nebivolol,
neostigmine, pasiréotide, pilocarpine, pindolol, propranolol, pyridostigmine, quinidine, rivastigmine, sotalol, tertatolol, thalidomide, timolol, verapamil)
+ AUTRES BRADYCARDISANTS
A prendre en compteRisque de bradycardie excessive (addition des effets).
+ FINGOLIMOD
Association DECONSEILLEE
Surveillance clinique et ECG continu pendant les 6 heures suivant la
première dose voire 2 heures de plus, jusqu'au lendemain si nécessaire.
Potentialisation des effets bradycardisants pouvant avoir des
conséquences fatales. Les bêta-bloquants sont d’autant plus à
risque qu’ils empêchent les mécanismes de compensation
adrénergique.
+ OZANIMOD
Association DECONSEILLEE
Surveillance clinique et ECG pendant au moins 6 heures.
Potentialisation des effets bradycardisants pouvant avoir des
conséquences fatales. Les bêta-bloquants sont d’autant plus à
risque qu’ils empêchent les mécanismes de compensation
adrénergique.
+ PONÉSIMOD
Association DECONSEILLEE
Surveillance clinique et ECG continu pendant les 4 heures suivant la
première dose, jusqu'au lendemain si nécessaire.
Potentialisation des effets bradycardisants pouvant avoir des
conséquences fatales. Les bêta-bloquants sont d’autant plus à
risque qu’ils empêchent les mécanismes de compensation
adrénergique.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
BRENTUXIMAB
Voir aussi : anticorps monoclonaux (hors anti-TNF alpha)
+ BLEOMYCINE
CONTRE-INDICATIONRisque de majoration de la toxicité pulmonaire.
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en compteAugmentation des concentrations du métabolite actif du
brentuximab, avec risque de neutropénie.
BUPRENORPHINE
Voir aussi : morphiniques - morphiniques agonistes-antagonistes - morphiniques en traitement de substitution - médicaments sédatifs
+ ATAZANAVIR
A prendre en compteRisque de majoration ou de diminution des effets de la
buprénorphine, à la fois par inhibition et accélération de son
métabolisme par l’inhibiteur de protéases.
+ BENZODIAZÉPINES ET APPARENTÉS
A prendre en compte
Evaluer attentivement le rapport bénéfice/risque de cette association.
Informer le patient de la nécessité de respecter les doses prescrites.
Avec la buprénorphine utilisée en traitement de substitution : risque
majoré de dépression respiratoire, pouvant être fatale.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
A prendre en compteRisque de majoration ou de diminution des effets de la
buprénorphine, à la fois par inhibition et accélération de son
métabolisme par l’inhibiteur de protéases.
+ ITRACONAZOLE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buprénorphine
pendant le traitement par l'inhibiteur et, le cas échéant, après son arrêt.
Augmentation des concentrations de buprénorphine par diminution
de son métabolisme hépatique, avec risque de majoration de ses
effets indésirables.
+ KETOCONAZOLE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buprénorphine
pendant le traitement par l'inhibiteur et, le cas échéant, après son arrêt.
Augmentation des concentrations de buprénorphine par diminution
de son métabolisme hépatique, avec risque de majoration de ses
effets indésirables.
44
BUPROPION
Voir aussi : médicaments abaissant le seuil épileptogène - médicaments à l'origine d'un syndrome sérotoninergique - sympathomimétiques indirects
+ CLOMIPRAMINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
clomipramine pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la clomipramine
par diminution de son métabolisme hépatique par le bupropion.
+ CODEINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ DESIPRAMINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
désipramine pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la désipramine
par diminution de son métabolisme hépatique par le bupropion.
+ IMAO-B
CONTRE-INDICATIONRisque de crises hypertensives.
+ MEQUITAZINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par le bupropion.
Avec le métoprolol utilisé dans l'insuffisance cardiaque : risque
d'augmentation des effets indésirables du métoprolol par diminution
de son métabolisme hépatique par le bupropion.
+ NORTRIPTYLINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
nortriptyline pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la nortriptyline
par diminution de son métabolisme hépatique par le bupropion.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
propafénone pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la propafénone
par diminution de son métabolisme hépatique par le bupropion.
+ TAMOXIFENE
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par le bupropion.
+ TETRABENAZINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ TRAMADOL
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ VÉMURAFÉNIB
A prendre en compteRisque de diminution des concentrations du bupropion, avec
augmentation de son métabolite actif et toxicité majorée.
BUSPIRONE
+ DIAZEPAM
A prendre en compteRisque de majoration des effets indésirables de la buspirone.
+ DILTIAZEM
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buspirone si
nécessaire.
Augmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique par le diltiazem, avec
augmentation de ses effets indésirables.
45
+ ERYTHROMYCINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique, avec majoration
importante de la sédation.
+ ITRACONAZOLE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique, avec majoration
importante de la sédation.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de la
buspirone par augmentation de son métabolisme par le millepertuis.
+ PAMPLEMOUSSE (JUS ET FRUIT)
A prendre en compteRisque de majoration des effets indésirables de la buspirone par
diminution de son métabolisme par le pamplemousse.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
buspirone pendant le traitement par rifampicine et après son arrêt.
Diminution des concentrations plasmatiques de la buspirone par
augmentation de son métabolisme hépatique par la rifampicine.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buspirone si
nécessaire.
Augmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique par le vérapamil, avec
augmentation de ses effets indésirables.
BUSULFAN
Voir aussi : cytotoxiques
+ DEFERASIROX
A prendre en compteRisque d’augmentation de la toxicité du busulfan par diminution de
sa clairance par le déférasirox.
+ ITRACONAZOLE
Association DECONSEILLEEAvec le busulfan à fortes doses : doublement des concentrations
de busulfan par l’itraconazole.
+ METRONIDAZOLE
Association DECONSEILLEEAvec le busulfan à fortes doses : doublement des concentrations
de busulfan par le métronidazole.
CABAZITAXEL
Voir aussi : cytotoxiques - substrats à risque du CYP3A4
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations du
cabazitaxel, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ INDUCTEURS ENZYMATIQUES
A prendre en compteDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
cabazitaxel pendant le traitement par l’inhibiteur enzymatique.
Risque de majoration des effets indésirables dose-dépendants du
cabazitaxel par inhibition de son métabolisme par l’inhibiteur
enzymatique.
46
CABOTEGRAVIR
Voir aussi : inhibiteurs d'intégrase
+ INDUCTEURS ENZYMATIQUES
CI - APEC
Contre-indication :
- avec la rifampicine, la carbamazépine, l'oxcarbazépine, la phénytoïne,
le phénobarbital
A prendre en compte :
- avec les autres inducteurs
Diminution importante des concentrations de cabotégravir avec la
rifampicine, avec risque de réduction de la réponse virologique.
CAFEINE
+ CIPROFLOXACINE
A prendre en compteAugmentation des concentrations plasmatiques de caféine, par
diminution de son métabolisme hépatique.
+ DIPYRIDAMOLE
Précaution d'emploi
Interrompre un traitement à base de caféine au moins 5 jours avant une
imagerie myocardique avec le dipyridamole et éviter la consommation
de café, thé, chocolat ou cola dans les 24 heures qui précèdent le test.
Avec le dipyridamole par voie injectable : réduction de l’effet
vasodilatateur du dipyridamole par la caféine.
+ ENOXACINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de caféine,
pouvant entraîner excitations et hallucinations, par diminution de
son métabolisme hépatique.
+ LITHIUM
A prendre en compteEn cas d’arrêt brutal de la consommation de café ou de
médicaments contenant de la caféine, risque d’augmentation de la
lithémie.
+ MEXILETINE
A prendre en compteAugmentation des concentrations plasmatiques de caféine, par
inhibition de son métabolisme hépatique par la méxilétine.
+ NORFLOXACINE
A prendre en compteAugmentation des concentrations plasmatiques de caféine, par
diminution du métabolisme hépatique de la caféine.
+ STIRIPENTOL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de caféine.
Augmentation possible des concentrations plasmatiques de la
caféine, avec risque de surdosage, par inhibition de son
métabolisme hépatique.
CALCITONINE
+ LITHIUM
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d’association.
Risque de baisse de l’efficacité du lithium par augmentation de son
élimination rénale par la calcitonine.
CALCIUM
+ BISPHOSPHONATES
Précaution d'emploi
Prendre les sels de calcium et antiacides à distance des
bisphosphonates (de 30 minutes au minimum à plus de 2 heures, si
possible, selon le bisphosphonate).
Pour les sels de calcium administrés par voie orale : diminution de
l'absorption digestive des bisphosphonates.
+ CIPROFLOXACINE
Précaution d'emploi
Prendre les sels de calcium à distance de la ciprofloxacine (plus de 2
heures, si possible).
Diminution de l'absorption digestive de la ciprofloxacine.
+ CYCLINES
Précaution d'emploi
Prendre les sels de calcium à distance des cyclines (plus de deux
heures, si possible).
Diminution de l'absorption digestive des cyclines.
47
+ DIGOXINE
CI - PE
Contre-indication :
- avec les sels de calcium IV, hormis supplémentation parentérale.
Précaution d'emploi :
- avec les sels de calcium par voie orale.
Surveillance clinique et, s'il y a lieu, contrôle de l'ECG et de la calcémie.
Risque de troubles du rythme graves, voire mortels avec les sels
de calcium administrés par voie IV.
+ DIURÉTIQUES THIAZIDIQUES ET APPARENTÉS
A prendre en compteRisque d'hypercalcémie par diminution de l'élimination urinaire du
calcium.
+ ESTRAMUSTINE
Précaution d'emploi
Prendre les sels de calcium à distance de l'estramustine (plus de 2
heures, si possible).
Diminution de l'absorption digestive de l'estramustine.
+ FER
Précaution d'emploi
Prendre les sels de fer à distance des repas et en l'absence de calcium.
Avec les sels de fer par voie orale : diminution de l'absorption
digestive des sels de fer.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Prendre les sels de calcium à distance des hormones thyroïdiennes
(plus de 2 heures, si possible).
Diminution de l’absorption digestive des hormones thyroïdiennes.
+ INHIBITEURS D'INTÉGRASE
Précaution d'emploi
Prendre les sels de calcium à distance de l’antirétroviral (plus de 2
heures, si possible).
Diminution de l'absorption digestive des inhibiteurs d’intégrase.
+ NORFLOXACINE
Précaution d'emploi
Prendre les sels de calcium à distance de la norfloxacine (plus de 2
heures, si possible).
Diminution de l'absorption digestive de la norflloxacine.
+ ROXADUSTAT
Précaution d'emploi
Prendre le roxadustat à distance des sels de calcium (plus de 1 heure,
si possible).
La prise de cation divalent peut diminuer l’absorption intestinale et,
potentiellement, l’efficacité du roxadustat pris simultanément.
+ STRONTIUM
Précaution d'emploi
Prendre le strontium à distance des sels de calcium (plus de deux
heures, si possible).
Avec les sels de calcium administrés par voie orale : diminution de
l'absorption digestive du strontium.
+ ZINC
Précaution d'emploi
Prendre les sels de calcium à distance du zinc (plus de 2 heures si
possible).
Diminution de l’absorption digestive du zinc par le calcium.
CANAKINUMAB
Voir aussi : anticorps monoclonaux (hors anti-TNF alpha)
+ ANTI-TNF ALPHA
Association DECONSEILLEERisque de majoration des infections graves.
CANNABIDIOL
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques de cannabidiol avec
risque de perte d’efficacité.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de cannabidiol avec
risque de perte d’efficacité.
48
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de cannabidiol avec
risque de perte d’efficacité.
CARBAMAZEPINE
Voir aussi : hyponatrémiants - inducteurs enzymatiques - inducteurs enzymatiques puissants
+ ACETAZOLAMIDE
Précaution d'emploi
Surveillance clinique et, si besoin, contrôle des concentrations
plasmatiques de carbamazépine et réduction éventuelle de sa
posologie.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
+ CIMETIDINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine, spécialement pendant les premiers jours de traitement
par la cimétidine.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : en début de traitement, augmentation des concentrations
plasmatiques de carbamazépine par inhibition de son métabolisme
hépatique par la cimétidine.
+ CLARITHROMYCINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage, par inhibition de son métabolisme
hépatique.
+ CLONAZEPAM
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation éventuelle
des posologies des deux anticonvulsivants.
Augmentation des concentrations plasmatiques du métabolite actif
de la carbamazépine. De plus, diminution des concentrations
plasmatiques du clonazépam par augmentation de son
métabolisme hépatique par la carbamazépine.
+ DANAZOL
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine.
Augmentation des concentrations plasmatiques de carbamazépine,
avec signes de surdosage.
+ DIGOXINE
Précaution d'emploi
Prudence dans l'interprétation des concentrations plasmatiques.
Augmentation des concentrations plasmatiques de carbamazépine
et diminution de la digoxinémie.
+ DIURÉTIQUES HYPOKALIÉMIANTS
Précaution d'emploi
Surveillance clinique et biologique. Si possible, utiliser une autre classe
de diurétiques.
Risque d'hyponatrémie symptomatique.
+ ERYTHROMYCINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de carbamazépine,
avec signes de surdosage, par inhibition de son métabolisme
hépatique.
+ ETHOSUXIMIDE
Précaution d'emploi
Surveillance clinique, dosage plasmatique de l'éthosuximide et
augmentation éventuelle de sa posologie.
Diminution des concentrations plasmatiques d'éthosuximide.
+ FELBAMATE
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation éventuelle
des posologies des deux anticonvulsivants.
Augmentation des concentrations plasmatiques du métabolite actif
de la carbamazépine. De plus, diminution des concentrations
plasmatiques de felbamate par augmentation de son métabolisme
hépatique par la carbamazépine.
+ FLUCONAZOLE
Précaution d'emploi
Adapter la posologie de carbamazépine, pendant et après l’arrêt du
traitement antifongique.
Pour des doses de fluconazole >= 200 mg par jour : augmentation
possible des effets indésirables de la carbamazépine.
+ FLUOXETINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
carbamazépine et réduction éventuelle de la posologie de la
carbamazépine pendant le traitement par l'antidépresseur
sérotoninergique et après son arrêt.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
49
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
carbamazépine et réduction éventuelle de la posologie de la
carbamazépine pendant le traitement par l'antidépresseur
sérotoninergique et après son arrêt.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
+ ISONIAZIDE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage par inhibition de son métabolisme
hépatique.
+ JOSAMYCINE
Précaution d'emploi
Surveillance clinique et, si besoin, dosage plasmatique et réduction
éventuelle de la posologie de la carbamazépine.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage, par diminution de son métabolisme
hépatique.
+ LAMOTRIGINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine.
Risque d'augmentation des effets neurologiques (vertiges, ataxie,
diplopie) de la carbamazépine lors de l'introduction de la
lamotrigine.
+ LITHIUM
Association DECONSEILLEERisque de neurotoxicité se manifestant par des troubles
cérébelleux, confusion, somnolence, ataxie. Ces troubles sont
réversibles à l'arrêt du traitement par le lithium.
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution des concentrations plasmatiques et de
l'efficacité de la carbamazepine.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Diminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par la carbamazépine.
+ OLANZAPINE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique de
l'olanzapine.
Risque de diminution des concentrations plasmatiques de
l'olanzapine et de son efficacité thérapeutique, par augmentation de
son métabolisme hépatique par la carbamazépine.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations plasmatiques de carbamazépine,
avec risque de surdosage, par inhibition de son métabolisme par le
pamplemousse.
+ PAROXETINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
carbamazépine et réduction éventuelle de la posologie de la
carbamazépine pendant le traitement par l'antidépresseur
sérotoninergique et après son arrêt.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
A prendre en compte
Prudence quant à l'interprétation des concentrations plasmatiques.
Diminution progressive des concentrations plasmatiques de
carbamazépine et de son métabolite actif sans modification
apparente de l'efficacité anticomitiale.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
A prendre en compte
Prudence dans l'interprétation des concentrations plasmatiques.
Réduction réciproque des concentrations plasmatiques
(augmentation du métabolisme sans modification apparente de
l'efficacité anticomitiale).
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques et
adaptation de la posologie de la carbamazépine pendant le traitement
par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
carbamazépine par augmentation de son métabolisme hépatique
par la rifampicine.
+ RISPERIDONE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique de la
rispéridone.
Risque de diminution de la fraction active de la rispéridone et de
son efficacité thérapeutique par augmentation de son métabolisme
hépatique par la carbamazépine.
50
+ SIMVASTATINE
Association DECONSEILLEEDiminution importante des concentrations plasmatiques de
simvastatine, par augmentation de son métabolisme hépatique.
+ TOPIRAMATE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique du
topiramate pendant le traitement par la carbamazépine et après son
arrêt.
Diminution des concentrations du topiramate avec risque de
moindre efficacité, par augmentation de son métabolisme
hépatique par la carbamazépine.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation de la
posologie des deux anticonvulsivants.
Augmentation des concentrations plasmatiques du métabolite actif
de la carbamazépine avec signes de surdosage. De plus,
diminution des concentrations plasmatiques d'acide valproïque par
augmentation de son métabolisme hépatique par la carbamazépine.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle des posologies des deux
médicaments.
Augmentation des concentrations de carbamazépine et de sa
neurotoxicité par inhibition de son métabolisme par le vérapamil.
De plus, diminution des concentrations du vérapamil par
augmentation de son métabolisme par la carbamazépine.
CARMUSTINE
Voir aussi : cytotoxiques
+ CIMETIDINE
Association DECONSEILLEEAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : toxicité médullaire accrue (inhibition du métabolisme de
la carmustine).
CARVEDILOL
Voir aussi : bradycardisants - bêta-bloquants dans l'insuffisance cardiaque - bêta-bloquants non cardio-sélectifs (y compris collyres) - médicaments abaissant la
pression artérielle
+ CIMETIDINE
CONTRE-INDICATION
Utiliser un autre antisécrétoire gastrique.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations du carvédilol, pouvant
être préjudiciables dans le cas du traitement de l'insuffisance
cardiaque, par diminution de son métabolisme hépatique par la
cimétidine.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique régulière et adaptation de la posologie du
carvédilol pendant le traitement par la rifampicine. A l'arrêt de la
rifampicine, risque de remontée importante des concentrations
plasmatiques de carvédilol imposant une réduction posologique et une
surveillance clinique étroite.
Diminution importante des concentrations plasmatiques du
carvédilol, par augmentation de son métabolisme hépatique par la
rifampicine.
CASPOFUNGINE
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
En cas de traitement par inducteur, maintenir la posologie à 70 mg par
jour dès le 2e jour.
Diminution des concentrations plasmatiques de caspofungine.
CEFALOTINE
+ AMINOSIDES
Précaution d'emploi
Surveillance de la fonction rénale.
L'augmentation de la néphrotoxicité des aminosides par la
céfalotine est discutée.
CEFAMANDOLE
Voir aussi : antabuse (réaction)
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la céphalosporine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
CEFAZOLINE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la céphalosporine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
51
CEFTRIAXONE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la céphalosporine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
CHLORDIAZEPOXIDE
Voir aussi : benzodiazépines et apparentés - médicaments sédatifs
+ CIMETIDINE
Précaution d'emploi
Avertir les patients de l'augmentation du risque en cas de conduite
automobile ou d'utilisation de machines.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : risque accru de somnolence.
CHLOROQUINE
Voir aussi : antiparasitaires susceptibles de donner des torsades de pointes - médicaments abaissant le seuil épileptogène - substances susceptibles de donner des
torsades de pointes
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt de la chloroquine.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ CIMETIDINE
A prendre en compteRalentissement de l’élimination de la chloroquine et risque de
surdosage.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
chloroquine et après son arrêt.
Risque d’hypothyroïdie clinique chez les patients substitués par
hormones thyroïdiennes.
CHLORPROMAZINE
Voir aussi : médicaments abaissant le seuil épileptogène - médicaments atropiniques - médicaments sédatifs - médicaments à l'origine d'une hypotension
orthostatique - neuroleptiques - neuroleptiques antipsychotiques (sauf clozapine) - neuroleptiques susceptibles de donner des torsades de pointes - substances
susceptibles de donner des torsades de pointes - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ INSULINE
Précaution d'emploi
Prévenir le patient et renforcer l'autosurveillance glycémique. Adapter
éventuellement la posologie de l'insuline pendant le traitement par le
neuroleptique et après son arrêt.
A fortes posologies (100 mg par jour de chlorpromazine) : élévation
de la glycémie (diminution de la libération de l'insuline).
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Prévenir le patient et renforcer l'autosurveillance glycémique. Adapter
éventuellement la posologie du neuroleptique pendant le traitement et
après son arrêt.
A fortes posologies (100 mg par jour de chlorpromazine) : élévation
de la glycémie (diminution de la libération de l'insuline).
CICLOSPORINE
Voir aussi : hyperkaliémiants - immunosuppresseurs - médicaments néphrotoxiques - médicaments à l'origine d'atteintes musculaires - substrats à risque du CYP3A4
+ ACIDE ASCORBIQUE
A prendre en compteRisque de diminution des concentrations sanguines de la
ciclosporine, notamment en cas d’association avec la vitamine E.
+ ACIDE URSODESOXYCHOLIQUE
A prendre en compteRisque de variation des concentrations sanguines de ciclosporine.
+ AFATINIB
Précaution d'emploi
Il est recommandé d’administrer la ciclosporine le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par la ciclosporine.
+ AMBRISENTAN
A prendre en compteDoublement des concentrations d’ambrisentan, avec majoration de
l’effet vasodilatateur (céphalées).
52
+ AMINOSIDES
A prendre en compteAugmentation de la créatininémie plus importante que sous
ciclosporine seule, avec majoration du risque néphrotoxique.
+ AMIODARONE
Association DECONSEILLEE
Dosage des concentrations sanguines de ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie de la ciclosporine pendant
le traitement par l'amiodarone.
Augmentation des concentrations sanguines de ciclosporine, par
diminution de son métabolisme hépatique, avec risque d'effets
néphrotoxiques.
+ AMPHOTERICINE B
A prendre en compteAvec l'amphotéricine B administrée par voie IV : augmentation de
la créatininémie plus importante que sous ciclosporine seule
(synergie des effets néphrotoxiques des deux substances).
+ ANALOGUES DE LA SOMATOSTATINE
Précaution d'emploi
Augmentation des doses de ciclosporine sous contrôle des
concentrations plasmatiques et réduction de la posologie après l'arrêt
du traitement par l'analogue de la somatostatine.
Avec la ciclosporine administrée par voie orale : baisse des
concentrations sanguines de ciclosporine (diminution de son
absorption intestinale).
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Précaution d'emploi
Surveiller la fonction rénale en début de traitement par l’AINS.
Risque d’addition des effets néphrotoxiques, notamment chez le
sujet âgé.
+ ATORVASTATINE
Précaution d'emploi
Ne pas dépasser la posologie de 10mg/jour d'atorvastatine. Si l'objectif
thérapeutique n'est pas atteint à cette posologie, utiliser une autre
statine non concernée par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme de
l'hypocholestérolémiant).
+ AZITHROMYCINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ BOSENTAN
CONTRE-INDICATIONDiminution importante des concentrations sanguines de la
ciclosporine et augmentation des concentrations plasmatiques de
bosentan.
+ CHLOROQUINE
Précaution d'emploi
Dosage des concentrations sanguines de ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt de la chloroquine.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ CIMETIDINE
A prendre en compteAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations sanguines de
ciclosporine.
+ CLINDAMYCINE
Précaution d'emploi
Contrôle renforcé des dosages sanguins de ciclosporine et
augmentation éventuelle de sa posologie.
Diminution des concentrations sanguines de l'immunosuppresseur
avec risque de perte de l'activité immunosuppressive.
+ COLCHICINE
Association DECONSEILLEERisque d’addition des effets indésirables neuromusculaires et
augmentation de la toxicité de la colchicine avec risque de
surdosage par inhibition de son élimination par la ciclosporine,
notamment en cas d’insuffisance rénale préexistante.
+ DABIGATRAN
CONTRE-INDICATIONAugmentation de plus du double des concentrations plasmatiques
de dabigatran, avec majoration du risque de saignement.
+ DANAZOL
Précaution d'emploi
Dosage des concentrations sanguines de ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l’association et
après son arrêt.
Augmentation des concentrations sanguines de ciclosporine par
inhibition de son métabolisme hépatique.
53
+ DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
Association DECONSEILLEEHyperkaliémie potentiellement létale, surtout lors d'une insuffisance
rénale (addition des effets hyperkaliémiants).
+ DIURÉTIQUES HYPOKALIÉMIANTS
A prendre en compteRisque d'augmentation de la créatininémie sans modification des
concentrations sanguines de ciclosporine, même en l'absence de
déplétion hydrosodée. Egalement, risque d'hyperuricémie et de
complications comme la goutte.
+ ÉDOXABAN
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
+ EVEROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines d’évérolimus, éventuellement
adaptation de la posologie et contrôle de la fonction rénale, pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines de l’évérolimus par la
ciclosporine. La néphrotoxicité de la ciclosporine est également
augmentée lors de l’association.
+ EZETIMIBE
Association DECONSEILLEED’une part, risque majoré d'effets indésirables (concentration-
dépendants) à type de rhabdomyolyse, par augmentation des
concentrations d’ézétimibe ; d’autre part, possible augmentation
des concentrations de ciclosporine.
+ FENOFIBRATE
Précaution d'emploi
Surveillance clinique et biologique de la fonction rénale, pendant et
après l'association.
Risque d'augmentation de la néphrotoxicité de la ciclosporine.
+ FIDAXOMICINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ FLUVASTATINE
Précaution d'emploi
Surveillance clinique et biologique pendant l’association.
Augmentation modérée des concentrations de fluvastatine, avec
risque musculaire non exclu.
+ GRAZOPREVIR + ELBASVIR
CONTRE-INDICATIONAugmentation des concentrations de grazoprévir et d’elbasvir.
+ JOSAMYCINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ LERCANIDIPINE
Précaution d'emploi
Décaler les prises des deux médicaments. Dosage des concentrations
sanguines de l'immunosuppresseur, et adaptation si nécessaire de sa
posologie pendant l'association et après son arrêt.
Augmentation modérée des concentrations sanguines de
l'immunosuppresseur et augmentation plus notable des
concentrations de lercanidipine.
+ METHOTREXATE
Précaution d'emploi
Dosage des concentrations sanguines de ciclosporine et de
méthotrexate. Adaptation posologique si nécessaire pendant
l'association et après son arrêt.
Augmentation de la toxicité du méthotrexate et de la ciclosporine
avec augmentation de la créatininémie : diminution réciproque des
clairances des deux médicaments.
+ METHYLPREDNISOLONE
A prendre en compteAvec la méthylprednisolone administrée par voie IV : augmentation
possible des concentrations sanguines de ciclosporine et de la
créatininémie. Mécanisme invoqué : diminution de l'élimination
hépatique de la ciclosporine.
+ MIDECAMYCINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
54
+ MIFAMURTIDE
CONTRE-INDICATIONRisque d'atteinte des macrophages spléniques et des cellules
phagocytaires mononuclées.
+ MODAFINIL
Association DECONSEILLEERisque de diminution des concentrations sanguines et de
l'efficacité de l'immunosuppresseur.
+ NIFEDIPINE
Association DECONSEILLEE
Utiliser une autre dihydropyridine.
Risque d'addition d'effets indésirables à type de gingivopathies.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par la ciclosporine.
+ ORLISTAT
Association DECONSEILLEE
Prendre l'orlistat à distance de la ciclosporine (au moins 3 heures).
Contrôle renforcé des dosages sanguins de ciclosporine, notamment en
début d’association, et lors d’augmentation éventuelle de la posologie
de l’orlistat.
Diminution des concentrations sanguines de ciclosporine par
diminution de son absorption intestinale, avec risque de perte de
l'activité immunosuppressive.
+ OZANIMOD
Association DECONSEILLEERisque d’augmentation des effets indésirables de l’ozanimod.
+ PITAVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, ou de néphrotoxicité, par diminution du
métabolisme de la pitavastatine.
+ POTASSIUM
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (
addition des effets hyperkaliémiants).
+ PRAVASTATINE
Précaution d'emploi
Surveillance clinique et biologique pendant l’association. Débuter le
traitement à la dose minimale de pravastatine.
Augmentation des concentrations de pravastatine, avec risque
musculaire non exclu.
+ PREDNISOLONE
A prendre en compteAugmentation des effets de la prednisolone : aspect cushingoïde,
réduction de la tolérance aux glucides (diminution de la clairance
de la prednisolone).
+ REPAGLINIDE
Association DECONSEILLEEAugmentation de plus du double des concentrations du répaglinide
par augmentation de son absorption.
+ ROSUVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, ou de néphrotoxicité, par diminution du
métabolisme de la rosuvastatine.
+ ROXITHROMYCINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ SIMVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par diminution du métabolisme de la
simvastatine.
55
+ SIROLIMUS
Précaution d'emploi
Il est recommandé d’administrer le sirolimus 4 heures après la
ciclosporine. Contrôle de la fonction rénale, pendant l’association et
après son arrêt.
Augmentation des concentrations sanguines de sirolimus par la
ciclosporine. La néphrotoxicité de la ciclosporine est également
augmentée lors de l’association.
+ SULFINPYRAZONE
Précaution d'emploi
Contrôle des concentrations sanguines de ciclosporine et adaptation
éventuelle de sa posologie pendant le traitement par sulfinpyrazone et
après son arrêt.
Diminution des concentrations sanguines de ciclosporine par
augmentation de son métabolisme par la sulfinpyrazone.
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ TÉNOFOVIR ALAFÉNAMIDE
Précaution d'emploi
En cas de co-administration avec la ciclosporine, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ TERBINAFINE
Précaution d'emploi
Contrôle des concentrations sanguines de ciclosporine et adaptation
éventuelle de sa posologie pendant le traitement par terbinafine et
après son arrêt.
Diminution des concentrations sanguines de ciclosporine.
+ TICLOPIDINE
Précaution d'emploi
Augmentation de la posologie de la ciclosporine sous contrôle des
concentrations sanguines. Réduction de la posologie en cas d'arrêt de
la ticlopidine.
Diminution des concentrations sanguines de ciclosporine.
+ TIGECYCLINE
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant le
traitement par la tigécycline.
Augmentation des concentrations sanguines de
l’immunosuppresseur, avec risque d'effets néphrotoxiques.
+ TRIMETHOPRIME
A prendre en compteAvec le triméthoprime (seul ou associé) par voie orale :
augmentation de la créatininémie avec diminution possible des
concentrations sanguines de ciclosporine.
Avec le trimethoprime (seul ou associé) par voie IV : la diminution
des concentrations sanguines de ciclosporine peut être très
importante avec disparition possible du pouvoir
immunosuppresseur.
+ VERAPAMIL
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l’association et
après son arrêt.
Augmentation des concentrations sanguines de la ciclosporine
(diminution de son métabolisme hépatique), et majoration du risque
de gingivopathies.
CIMETIDINE
Voir aussi : antisécrétoires antihistaminiques H2 - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ALFENTANIL
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par la
cimétidine.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de l'effet dépresseur respiratoire de
l'analgésique opiacé par diminution de son métabolisme hépatique.
+ ANTIVITAMINES K
A prendre en compteAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de l'effet de l'antivitamine K et du risque
hémorragique (diminution de son métabolisme hépatique).
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine, spécialement pendant les premiers jours de traitement
par la cimétidine.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : en début de traitement, augmentation des concentrations
plasmatiques de carbamazépine par inhibition de son métabolisme
hépatique par la cimétidine.
+ CARMUSTINE
Association DECONSEILLEEAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : toxicité médullaire accrue (inhibition du métabolisme de
la carmustine).
56
+ CARVEDILOL
CONTRE-INDICATION
Utiliser un autre antisécrétoire gastrique.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations du carvédilol, pouvant
être préjudiciables dans le cas du traitement de l'insuffisance
cardiaque, par diminution de son métabolisme hépatique par la
cimétidine.
+ CHLORDIAZEPOXIDE
Précaution d'emploi
Avertir les patients de l'augmentation du risque en cas de conduite
automobile ou d'utilisation de machines.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : risque accru de somnolence.
+ CHLOROQUINE
A prendre en compteRalentissement de l’élimination de la chloroquine et risque de
surdosage.
+ CICLOSPORINE
A prendre en compteAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations sanguines de
ciclosporine.
+ DIAZEPAM
Précaution d'emploi
Avertir les patients de l'augmentation du risque en cas de conduite
automobile ou d'utilisation de machines.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : risque accru de somnolence.
+ LIDOCAINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement des concentrations
plasmatiques de la lidocaïne ; s'il y a lieu, adaptation de la posologie de
la lidocaïne pendant le traitement par la cimétidine et après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations plasmatiques de
lidocaïne avec risque d'effets indésirables neurologiques et
cardiaques (inhibition du métabolisme hépatique de la lidocaïne).
+ LOMUSTINE
Association DECONSEILLEEAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : toxicité médullaire accrue (inhibition du métabolisme de
la lomustine).
+ METHADONE
Précaution d'emploi
Surveillance clinique et électrocardiographique renforcée ; si besoin,
adaptation de la posologie de la méthadone pendant le traitement par la
cimétidine et après son arrêt.
Augmentation des concentrations plasmatiques de méthadone
avec surdosage et risque majoré d’allongement de l’intervalle QT et
de troubles du rythme ventriculaire, notamment de torsades de
pointes.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par la cimétidine.
Avec le métoprolol utilisé dans l'insuffisance cardiaque, et la
cimétidine utilisée à des doses supérieures ou égales à 800 mg/j :
augmentation des concentrations du métoprolol, pouvant être
préjudiciables dans le cas du traitement de l'insuffisance cardiaque,
par diminution de son métabolisme hépatique par la cimétidine.
+ MOCLOBEMIDE
Précaution d'emploi
Surveillance clinique avec adaptation éventuelle de la posologie de
moclobémide.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations du moclobémide, par
diminution de son métabolisme hépatique.
+ NIFEDIPINE
Précaution d'emploi
Surveillance clinique accrue : adapter la posologie de la nifédipine
pendant le tratiement par la cimétidine et après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de l'effet hypotenseur de la nifédipine par
inhibition de son métabolisme hépatique par la cimétidine.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite, dosage
des concentrations plasmatiques de phénytoïne et adaptation
éventuelle de sa posologie pendant le traitement par la cimétidine et
après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations plasmatiques de
phénytoïne avec possibilité d'apparition des signes habituels de
surdosage.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie. S'il y a
lieu, adaptation de la théophylline pendant le traitement par la
cimétidine et après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de la théophyllinémie avec risque de
surdosage (diminution du métabolisme de la théophylline).
CINACALCET
+ CODEINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
57
+ DEXTROMETHORPHANE
CONTRE-INDICATIONAugmentation très importante des concentrations plasmatiques de
dextrométhorphane avec risque de surdosage, par diminution de
son métabolisme hépatique par le cinacalcet.
+ ÉTELCALCÉTIDE
Association DECONSEILLEERisque d’hypocalcémie sévère.
+ MEQUITAZINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique et réduction de la posologie du métroprolol
pendant le traitement par cinacalcet.
Augmentation des concentrations plasmatiques de métroprolol
avec risque de surdosage, par diminution de son métabolisme
hépatique par le cinacalcet.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par cinacalcet.
Augmentation des concentrations plasmatiques de propafénone
avec risque de surdosage, par diminution de son métabolisme
hépatique par le cinacalcet.
+ TETRABENAZINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ TRAMADOL
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
CIPROFLOXACINE
Voir aussi : fluoroquinolones - médicaments abaissant le seuil épileptogène - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et
adsorbants
+ AGOMELATINE
Association DECONSEILLEEAugmentation des concentrations d'agomélatine, avec risque de
majoration des effets indésirables.
+ CAFEINE
A prendre en compteAugmentation des concentrations plasmatiques de caféine, par
diminution de son métabolisme hépatique.
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium à distance de la ciprofloxacine (plus de 2
heures, si possible).
Diminution de l'absorption digestive de la ciprofloxacine.
+ CLOZAPINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
clozapine pendant le traitement par la ciprofloxacine et après son arrêt.
Augmentation des concentrations de clozapine avec risque de
surdosage, par diminution de son métabolisme hépatique par la
ciprofloxacine.
+ METHOTREXATE
Association DECONSEILLEEAugmentation de la toxicité du méthotrexate par inhibition de sa
sécrétion tubulaire rénale par la ciprofloxacine.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
l’anticonvulsivant pendant le traitement par ciprofloxacine et après son
arrêt.
Variation, éventuellement importante, des concentrations de
phénytoïne en cas de traitement par la ciprofloxacine.
+ ROPINIROLE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie du
ropinirole pendant le traitement par la ciprofloxacine et après son arrêt.
Augmentation des concentrations de ropinirole avec risque de
surdosage, par diminution de son métabolisme hépatique par la
ciprofloxacine.
58
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Augmentation de la théophyllinémie avec risque de surdosage, par
diminution de son métabolisme hépatique par la ciprofloxacine.
CITRATES
(citrate de gallium [67ga], dicitrate trimagnesien, potassium (citrate de), sodium (citrate de), sodium (citrate diacide de))
+ ALUMINIUM (SELS)
Précaution d'emploi
Prendre les topiques gastro-intestinaux à base d'aluminium à distance
des citrates (plus de 2 heures si possible), y compris les citrates
naturels (jus d'agrumes).
Risque de facilitation du passage systémique de l’aluminium,
notamment en cas de fonction rénale altérée.
CLADRIBINE
Voir aussi : cytotoxiques
+ LAMIVUDINE
Association DECONSEILLEERisque de diminution de l’efficacité de la cladribine par la
lamivudine.
CLARITHROMYCINE
Voir aussi : inhibiteurs puissants du CYP3A4 - macrolides (sauf spiramycine)
+ ATAZANAVIR
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Augmentation des concentrations plasmatiques de clarithromycine
et inhibition de la formation de son métabolite actif.
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholesterolémiant.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage, par inhibition de son métabolisme
hépatique.
+ ETRAVIRINE
A prendre en compteDans le traitement des infections à Mycobacterium avium complex,
risque de diminution de l’efficacité de la clarithromycine par
augmentation de son métabolisme hépatique par l’étravirine.
+ FIDAXOMICINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Augmentation des concentrations de la clarithromycine et de son
métabolite actif par diminution de son métabolisme hépatique par
l'inhibiteur de protéases.
+ LINEZOLIDE
A prendre en compteRisque de majoration des effets indésirables du linézolide par la
clarithromycine, par augmentation de son absorption.
+ PRAVASTATINE
Précaution d'emploi
Surveillance clinique et biologique pendant le traitement par
l'antibiotique.
Augmentation de la concentration plasmatique de la pravastatine
par la clarithromycine.
59
+ REPAGLINIDE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie de l'hypoglycémiant pendant le traitement
par la clarithromycine.
Risque d'hypoglycémie par augmentation des concentrations
plasmatiques du répaglinide.
+ RIFABUTINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'augmentation des effets indésirables de la rifabutine
(uvéites) par augmentation de ses concentrations et de celle de
son métabolite actif par la clarithromycine. De plus, augmentation
du métabolisme de la clarithromycine par la rifabutine, avec
augmentation des concentrations de son métabolite actif.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Diminution des concentrations plasmatiques et risque de baisse de
l'efficacité de la clarithromycine, notamment chez le patient HIV,
par augmentation de son métabolisme hépatique par la rifampicine.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide hypoglycémiant pendant le
traitement par la clarithromycine.
Risque d'hypoglycémie par augmentation des concentrations
plasmatiques de l’antidiabétique.
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
A prendre en compteRisque d'augmentation de la théophyllinémie, particulièrement chez
l'enfant.
+ VENLAFAXINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
CLINDAMYCINE
Voir aussi : lincosanides - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par clindamycine et après son
arrêt.
Augmentation de l’effet de l’antivitamine K et du risque
hémorragique.
+ CICLOSPORINE
Précaution d'emploi
Contrôle renforcé des dosages sanguins de ciclosporine et
augmentation éventuelle de sa posologie.
Diminution des concentrations sanguines de l'immunosuppresseur
avec risque de perte de l'activité immunosuppressive.
+ TACROLIMUS
Précaution d'emploi
Contrôle renforcé des dosages sanguins de tacrolimus et augmentation
éventuelle de sa posologie.
Diminution des concentrations sanguines de l'immunosuppresseur,
avec risque de perte de l'activité immunosuppressive.
CLOBAZAM
Voir aussi : benzodiazépines et apparentés - médicaments sédatifs
+ STIRIPENTOL
Précaution d'emploi
Surveillance clinique, dosage plasmatique, lorsque cela est possible, de
l'anticonvulsivant associé au stiripentol et éventuelle adaptation
posologique de l'anticonvulsivant associé.
Augmentation des concentrations plasmatiques de ces
anticonvulsivants, avec risque de surdosage, par inhibition de leur
métabolisme hépatique.
60
CLOMIPRAMINE
Voir aussi : antidépresseurs imipraminiques - médicaments abaissant le seuil épileptogène - médicaments atropiniques - médicaments mixtes adrénergiques-
sérotoninergiques - médicaments à l'origine d'un syndrome sérotoninergique - médicaments à l'origine d'une hypotension orthostatique
+ BUPROPION
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
clomipramine pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la clomipramine
par diminution de son métabolisme hépatique par le bupropion.
CLONAZEPAM
Voir aussi : benzodiazépines et apparentés - médicaments sédatifs
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation éventuelle
des posologies des deux anticonvulsivants.
Augmentation des concentrations plasmatiques du métabolite actif
de la carbamazépine. De plus, diminution des concentrations
plasmatiques du clonazépam par augmentation de son
métabolisme hépatique par la carbamazépine.
CLOPIDOGREL
Voir aussi : antiagrégants plaquettaires
+ ACIDE ACETYLSALICYLIQUE
ASDEC - PE
Association déconseillée :
- en dehors des indications validées pour cette association dans les
syndromes coronariens aigus.
Précaution d'emploi :
- dans les indications validées pour cette association dans les
syndromes coronariens aigus. Surveillance clinique.
Majoration du risque hémorragique par addition des activités
antiagrégantes plaquettaires.
+ OZANIMOD
A prendre en compteRisque d’augmentation des concentrations des métabolites actifs
de l’onazimod.
+ PACLITAXEL
A prendre en compteAugmentation des concentrations du paclitaxel par le clopidogrel,
avec risque de majoration des effets indésirables.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage (inhibition du métabolisme de la
+ REPAGLINIDE
A prendre en compteAugmentation des concentrations du répaglinide par le clopidogrel,
avec risque de majoration des effets indésirables.
+ SELEXIPAG
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
CLOZAPINE
Voir aussi : médicaments atropiniques - médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - médicaments à risque lors du sevrage
tabagique - neuroleptiques
+ BENZODIAZÉPINES ET APPARENTÉS
A prendre en compteRisque accru de collapsus avec arrêt respiratoire et / ou cardiaque.
+ CIPROFLOXACINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
clozapine pendant le traitement par la ciprofloxacine et après son arrêt.
Augmentation des concentrations de clozapine avec risque de
surdosage, par diminution de son métabolisme hépatique par la
ciprofloxacine.
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie de la
clozapine pendant le traitement par la fluvoxamine et après son arrêt.
Augmentation des concentrations plasmatiques de clozapine avec
signes de surdosage.
61
+ INDUCTEURS ENZYMATIQUES PUISSANTS
ASDEC - PE
Association déconseillée:
- avec la carbamazépine, l'apalutamide, l'enzalutamide
Précaution d'emploi:
- Avec la phénytoïne, la fosphénytoïne, la primidone, le phénobarbital.
Surveillance clinique et adaptation posologique de la clozapine pendant
l’association et après l’arrêt de l’inducteur
- Avec l'apalutamide, l'enzalutamide : risque vraisemblablement modéré
Diminution des concentrations plasmatiques de clozapine avec
risque de perte d’efficacité.
De plus, avec la carbamazépine, risque de majoration des effets
hématologiques graves.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque d’inefficacité du traitement antipsychotique (diminution des
concentrations plasmatiques de clozapine par augmentation de son
métabolisme hépatique).
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et augmentation éventuelle de la posologie de la
clozapine durant le traitement par la rifampicine.
Risque d'inefficacité du traitement antipsychotique (diminution des
concentrations plasmatiques de clozapine par augmentation de son
métabolisme hépatique).
COBICISTAT
Voir aussi : inhibiteurs puissants du CYP3A4
+ AMIODARONE
CONTRE-INDICATIONRisque de majoration des effets indésirables de l'amiodarone par
diminution de son métabolisme par le cobicistat.
+ ETRAVIRINE
Association DECONSEILLEERisque de diminution des concentrations plasmatiques du
cobicistat par l’étravirine.
+ GLUCOCORTICOÏDES PAR VOIE INTRA-ARTICULAIRE ET MÉTABOLISÉS
Précaution d'emploi
Préférer un corticoïde non CYP3A4-dépendant (hydrocortisone).
Décrit chez des patients HIV. Risque d’insuffisance surrénale
aiguë, même en cas d’injection unique. L’articulation peut
constituer un réservoir relarguant de façon continue le corticoïde
CYP3A4-dépendant dans la circulation générale, avec
augmentation possiblement très importante des concentrations du
corticoïde, à l’origine d’une freination de la réponse hypothalamo-
hypophysaire.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
CONTRE-INDICATIONRisque de diminution de l’efficacité du cobicistat par augmentation
de son métabolisme par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en compte
Pour connaître les risques et les niveaux de contrainte de chaque
interaction, il convient de se reporter aux AMM specifiques à chaque
spécialité.
Risque d’augmentation des concentrations plasmatiques du
cobicistat ou de l’inhibiteur du CYP3A4.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution de l’efficacité du cobicistat par augmentation
de son métabolisme par l’inducteur.
+ QUINIDINE
CONTRE-INDICATION
Surveillance clinique.
Risque de majoration des effets indésirables de la quinidine par
diminution de son métabolisme par le cobicistat.
+ RIFABUTINE
Précaution d'emploi
Réduction de la dose de rifabutine (150 mg 1 jour sur deux).
Surveillance clinique et biologique régulière, notamment en début
d'association.
Augmentation très importante du métabolite de la rifabutine, avec
risque de majoration de sa toxicité (uvéites, neutropénies). Par
ailleurs, possible diminution des concentrations de cobicistat.
+ RIFAMPICINE
CONTRE-INDICATIONRisque de diminution de l’efficacité du cobicistat par augmentation
de son métabolisme par l’inducteur.
62
+ TÉNOFOVIR ALAFÉNAMIDE
Précaution d'emploi
En cas de co-administration, la dose de ténofovir alafénamide doit être
limitée à 10 mg par jour. L’association avec les autres inhibiteurs de
protéases du VIH n’a pas été étudiée.
Avec l'atazanavir, le darunavir ou le lopinavir boostés par cobicistat,
augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
COBIMÉTINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés - substrats à risque du CYP3A4
+ ANTIAGRÉGANTS PLAQUETTAIRES
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ ANTICOAGULANTS ORAUX
Précaution d'emploi
Surveillance clinique et le cas échéant, contrôle plus fréquent de l'INR.
Augmentation du risque hémorragique.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ DÉFIBROTIDE
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ HÉPARINES
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
A prendre en compteRisque majoré de rhabdomyolyse.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ PENTOXIFYLLINE
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
COCAINE
Voir aussi : substances susceptibles de donner des torsades de pointes - torsadogènes (sauf arsénieux, antiparasitaires, neuroleptiques, méthadone...)
+ DISULFIRAME
A prendre en compteAugmentation des concentrations de cocaïne par diminution de son
métabolisme par le disulfirame, avec risque majoré de survenue de
torsades de pointes.
CODEINE
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier II - antitussifs morphiniques vrais - morphiniques - médicaments sédatifs
+ BUPROPION
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
63
+ CINACALCET
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ DULOXETINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ FLUOXETINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ PAROXETINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ QUINIDINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ TERBINAFINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
COLCHICINE
Voir aussi : médicaments à l'origine d'atteintes musculaires
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la colchicine et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ CICLOSPORINE
Association DECONSEILLEERisque d’addition des effets indésirables neuromusculaires et
augmentation de la toxicité de la colchicine avec risque de
surdosage par inhibition de son élimination par la ciclosporine,
notamment en cas d’insuffisance rénale préexistante.
+ FIBRATES
Précaution d'emploi
Surveillance clinique et biologique, particulièrement au début de
l’association.
Risque de majoration des effets indésirables musculaires de ces
substances, et notamment de rhabdomyolyse.
+ FLUCONAZOLE
Association DECONSEILLEEAugmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Précaution d'emploi
Surveillance clinique et biologique, notamment au début de l'association.
Risque de majoration des effets indésirables musculaires de ces
substances, et notamment de rhabdomyolyse.
+ INHIBITEURS PUISSANTS DU CYP3A4
CI - ASDEC
Contre-indication :
- avec les macrolides
Association déconseillée :
- avec les antifongiques azolés, les inhibiteurs de protéases boostés par
ritonavir et le cobicistat
Augmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
+ MACROLIDES (SAUF SPIRAMYCINE)
CONTRE-INDICATIONAugmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
64
+ OMBITASVIR + PARITAPRÉVIR
CI - ASDEC
Contre-indication:
- chez les patients insuffisants rénaux et/ou hépatiques.
Association déconseillée
- chez les patients ayant une fonction rénale et hépatique normale. Si
l’association s'avère nécessaire, une réduction de la dose de colchicine
ou une interruption du traitement par la colchicine est recommandée.
Augmentation des concentrations plasmatiques de la colchicine par
diminution de son métabolisme hépatique par la bithérapie.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
colchicine par augmentation de son absorption intestinale par le
ponatinib.
+ PRISTINAMYCINE
CONTRE-INDICATIONAugmentation des effets indésirables de la colchicine aux
conséquences potentiellement fatales.
+ ROLAPITANT
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
+ VERAPAMIL
Association DECONSEILLEERisque de majoration des effets indésirables de la colchicine, par
augmentation de ses concentrations plasmatiques par le vérapamil.
COLISTINE
Voir aussi : médicaments néphrotoxiques
+ CURARES
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
CORTICOÏDES
(betamethasone, cortisone, cortivazol, desoxycortone, dexamethasone, fludrocortisone, hydrocortisone, methylprednisolone, prednisolone, prednisone, tetracosactide,
triamcinolone)
+ MIFAMURTIDE
Association DECONSEILLEERisque de moindre efficacité du mifamurtide.
CORTICOÏDES (VOIE INTRA-ARTICULAIRE)
(betamethasone, dexamethasone, méthylprednisolone, prednisolone, triamcinolone)
+ RITONAVIR
A prendre en compte
Préférer un corticoïde non CYP3A4-dépendant (hydrocortisone)
Décrit chez des patients HIV.
Risque d’insuffisance surrénale aiguë, même en cas d’injection
unique.
L’articulation peut constituer un réservoir relarguant de façon
continue le corticoïde CYP3A4-dépendant dans la circulation
générale, avec augmentation possiblement très importante des
concentrations du corticoïde à l’origine d’une freination de la
réponse hypothalamo-hypophysaire.
CORTICOÏDES MÉTABOLISÉS, NOTAMMENT INHALÉS
(budesonide, ciclesonide, dexamethasone, fluticasone, methylprednisolone, mometasone, prednisolone, prednisone, triamcinolone)
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Préférer un corticoïde non métabolisé.
En cas d’utilisation prolongée par voie orale ou inhalée :
augmentation des concentrations plasmatiques du corticoïde par
diminution de son métabolisme hépatique par l’inhibiteur, avec
risque d’apparition d’un syndrome cushingoïde
voire d’une insuffisance surrénalienne.
CRIZOTINIB
Voir aussi : bradycardisants - inhibiteurs de tyrosine kinases métabolisés - substances susceptibles de donner des torsades de pointes - substrats à risque du CYP3A4
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le crizotinib.
65
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Association DECONSEILLEE
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SUBSTRATS À RISQUE DU CYP3A4
Association DECONSEILLEERisque de majoration de la toxicité de ces molécules par diminution
de leur métabolisme et/ou augmentation de leur biodisponibilité par
le crizotinib.
CURARES
Certaines substances peuvent modifier l'intensité et/ou la durée de l'effet des curares non dépolarisants.
Les médicaments susceptibles de potentialiser l'action des curares non dépolarisants sont :
- les anesthésiques volatils tels que isoflurane, enflurane, desflurane, sévoflurane ou halothane,
- les anesthésiques locaux,
- certains antibiotiques (aminosides, polymyxines, lincosanides),
- le sulfate de magnésium (IV),
- les antagonistes du calcium
- les médicaments aggravant ou révélant un syndrome myasthénique, comme les fluoroquinolones, la télithromycine, l’érythromycine IV, la quinidine ou le lithium..
Les médicaments susceptibles de diminuer l'action des curares non dépolarisants sont :
- la phénytoïne ou la carbamazépine, en administration chronique
L’utilisation de curares chez des patients recevant des corticoïdes injectables expose au risque de myopathie, éventuellement longue.
En principe, un monitoring maintenu jusqu'à complète décurarisation permet d'éviter la survenue d'une interaction. Toutefois, une recurarisation non prévue pourrait se
produire, dans le cas d'une couverture antibiotique post-opératoire avec un aminoside, par exemple.
(atracurium, cisatracurium, mivacurium, rocuronium, suxamethonium, vecuronium)
+ AMINOSIDES
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
+ COLISTINE
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
+ LINCOSANIDES
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
+ POLYMYXINE B
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
CURARES NON DÉPOLARISANTS
(atracurium, cisatracurium, rocuronium, vecuronium)
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
A prendre en compteAvec les glucocorticoïdes par voie IV : risque de myopathie sévère,
réversible après un délai éventuellement long (plusieurs mois).
CYANOCOBALAMINE
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compteRisque de carence en cyanocobalamine après traitement prolongé
(quelques années), la réduction de l’acidité gastrique par ces
médicaments pouvant diminuer l’absorption digestive de la
vitamine B12.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compteRisque de carence en cyanocobalamine après traitement prolongé
(quelques années), la réduction de l’acidité gastrique par ces
médicaments pouvant diminuer l’absorption digestive de la
vitamine B12.
66
CYCLINES
(chlortetracycline, déméclocycline, doxycycline, lymecycline, methylenecycline, minocycline, oxytetracycline, tetracycline, tigecycline)
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la cycline et après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique (pour la tigécycline, effet direct sur la coagulation
et/ou les systèmes fibrinolytiques).
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium à distance des cyclines (plus de deux
heures, si possible).
Diminution de l'absorption digestive des cyclines.
+ FER
Précaution d'emploi
Prendre les sels de fer à distance des cyclines (plus de 2 heures, si
possible).
Diminution de l'absorption digestive des cyclines et du fer
+ RÉTINOÏDES
CONTRE-INDICATIONRisque d'hypertension intracrânienne.
+ STRONTIUM
Précaution d'emploi
Prendre le strontium à distance des cyclines (plus de deux heures, si
possible).
Diminution de l'absorption digestive du strontium.
+ VITAMINE A
CONTRE-INDICATIONEn cas d'apport de 10,000 UI/j et plus : risque d’hypertension
intracrânienne.
+ ZINC
Précaution d'emploi
Prendre les sels de zinc à distance des cyclines (plus de 2 heures si
possible).
Diminution de l'absorption digestive des cyclines.
CYCLOPHOSPHAMIDE
Voir aussi : cytotoxiques
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
métabolite actif du cyclophosphamide par l'inducteur, et donc de sa
toxicité.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques du
métabolite actif du cyclophosphamide par le millepertuis, et donc
de sa toxicité.
+ PENTOSTATINE
Association DECONSEILLEEMajoration du risque de toxicité pulmonaire pouvant être fatale.
CYPROHEPTADINE
Voir aussi : médicaments atropiniques - médicaments sédatifs
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteRisque de diminution de l'efficacité de l'antidépresseur.
CYPROTERONE
Voir aussi : médicaments à l'origine d'un hypogonadisme masculin
+ APREPITANT
Précaution d'emploi
Dans son utilisation comme contraceptif hormonal :
Utiliser une méthode de contraception fiable, additionnelle ou
alternative, pendant la durée de l'association.
Risque de diminution des concentrations de la cyprotérone avec
risque de moindre efficacité contraceptive.
67
+ BOSENTAN
Précaution d'emploi
Dans ses indications comme anti-androgène, surveillance clinique et si
possible adaptation de la posologie de la cyprotérone pendant
l'administration avec le bosentan et après son arrêt.
Dans son utilisation comme contraceptif hormonal, utiliser une méthode
de contraception fiable, additionnelle ou alternative pendant la durée de
l'association.
Risque de diminution de l'efficacité de la cyprotérone.
+ INDUCTEURS ENZYMATIQUES
ASDEC - PE
Association déconseillée:
- dans son utilisation comme contraceptif hormonal: utiliser de
préférence une autre méthode de contraception en particulier de type
mécanique, pendant la durée de l'association et un cycle suivant.
Précaution d'emploi
- dans ses indications comme anti-androgène: surveillance clinique et
adaptation éventuelle de la posologie de la cyprotérone pendant
l'association et après son arrêt.
Risque de diminution de l'efficacité de la cyprotérone.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
ASDEC - PE
Association déconseillée
- dans son utilisation comme contraceptif hormonal: utiliser de
préférence une autre méthode de contraception en particulier de type
mécanique, pendant la durée de l'association et un cycle suivant.
Précaution d'emploi
- dans ses indications comme anti-androgène: surveillance clinique et
adaptation éventuelle de la posologie de la cyprotérone pendant
l'association et après son arrêt.
Risque de diminution de l'efficacité de la cyprotérone.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution de l'efficacité de la cyprotérone, par
augmentation de son métabolisme hépatique par le millepertuis.
+ PÉRAMPANEL
Association DECONSEILLEE
Dans son utilisation comme contraceptif hormonal: utiliser de
préférence une autre méthode de contraception en particulier de type
mécanique, pendant la durée de l'association et un cycle suivant.
Pour des doses de pérampanel > ou = à 12 mg/jour, risque de
diminution de l'efficacité de la cyprotérone.
+ ULIPRISTAL
ASDEC - APEC
Association déconseillée
Dans l'utilisation à visée contraceptive de la cyprotérone
- Dans l'indication contraception d'urgence de l'ulipristal
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception additionnelle de type mécanique
pendant les 12 jours qui suivent la (dernière) prise de l’ulipristal (au cas
où il y en aurait eu plus d’une).
- Dans l’indication fibrome de l'ulipristal :
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception de type mécanique pendant les 7
premiers jours de la contraception hormonale.
Association à prendre en compte
Lorsque la cyprotérone n'est pas à visée contraceptive.
Dans l'indication contraception d'urgence de l'ulipristal :
Antagonisme des effets de l’ulipristal en cas de reprise d’un
contraceptif hormonal moins de 5 jours après la prise de la
contraception d’urgence.
Dans l’indication fibrome de l'ulipristal :
Antagonisme réciproque des effets de l’ulipristal et du progestatif,
avec risque d’inefficacité.
CYTOTOXIQUES
(altretamine, amsacrine, asparaginase, azacitidine, azathioprine, bendamustine, bleomycine, bortezomib, busulfan, cabazitaxel, capecitabine, carboplatine,
carmustine, chlorambucil, cisplatine, cladribine, clofarabine, cyclophosphamide, cytarabine, dacarbazine, dactinomycine, daunorubicine, décitabine, dexrazoxane,
docetaxel, doxorubicine, epirubicine, éribuline, estramustine, etoposide, fludarabine, fluorouracile, fotemustine, gemcitabine, giméracil, hydroxycarbamide, idarubicine,
ifosfamide, irinotecan, lomustine, melphalan, mercaptopurine, methotrexate, mitomycine c, mitoxantrone, nélarabine, otéracil, oxaliplatine, paclitaxel, pemetrexed,
pentostatine, pipobroman, pixantrone, procarbazine, raltitrexed, streptozocine, tegafur, temozolomide, thiotepa, tioguanine, topotecane, vinblastine, vincristine,
vindesine, vinflunine, vinorelbine)
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR.
Augmentation du risque thrombotique et hémorragique au cours
des affections tumorales. De surcroit, possible interaction entre les
AVK et la chimiothérapie.
+ FLUCYTOSINE
A prendre en compteRisque de majoration de la toxicité hématologique
68
+ IMMUNOSUPPRESSEURS
A prendre en compteImmunodépression excessive avec risque de syndrome lympho-
prolifératif.
+ OLAPARIB
Association DECONSEILLEERisque de majoration de l’effet myélosuppresseur du cytotoxique
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Association DECONSEILLEERisque de survenue de convulsions par diminution de l'absorption
digestive de la seule phénytoïne par le cytotoxique, ou bien risque
de majoration de la toxicité ou de perte d'efficacité du cytotoxique
par augmentation de son métabolisme hépatique par la phénytoïne
ou la fosphénytoïne.
+ VACCINS VIVANTS ATTÉNUÉS
CONTRE-INDICATION
- Et pendant les 6 mois suivant l'arrêt de la chimiothérapie.
- Et, à l'exception de l'hydroxycarbamide dans son indication chez le
patient drépanocytaire.
Risque de maladie vaccinale généralisée éventuellement mortelle.
DABIGATRAN
Voir aussi : anticoagulants oraux
+ AMIODARONE
Précaution d'emploi
Dans l'indication post-chirurgicale : surveillance clinique et adaptation
de la posologie du dabigatran si nécessaire, sans excéder 150 mg/j.
Augmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
+ CICLOSPORINE
CONTRE-INDICATIONAugmentation de plus du double des concentrations plasmatiques
de dabigatran, avec majoration du risque de saignement.
+ DRONEDARONE
CONTRE-INDICATIONDoublement des concentrations plasmatiques de dabigatran, avec
majoration du risque de saignement.
+ GLÉCAPRÉVIR + PIBRENTASVIR
CONTRE-INDICATIONDoublement des concentrations plasmatiques de dabigatran, avec
majoration du risque de saignements.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques de dabigatran, avec
risque de diminution de l'effet thérapeutique.
+ ITRACONAZOLE
CONTRE-INDICATIONAugmentation de plus du double des concentrations plasmatiques
de dabigatran, avec majoration du risque de saignement.
+ KETOCONAZOLE
CONTRE-INDICATIONAugmentation de plus du double des concentrations plasmatiques
de dabigatran, avec majoration du risque de saignement.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
dabigatran par augmentation de son absorption intestinale par le
ponatinib.
+ QUINIDINE
Précaution d'emploi
Dans l'indication post-chirurgicale : surveillance clinique et adaptation
de la posologie du dabigatran à 150 mg/j en une prise.
Augmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de dabigatran, avec
risque de diminution de l'effet thérapeutique.
69
+ ROLAPITANT
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
dabigatran par augmentation de son absorption intestinale par le
rolapitant.
+ TACROLIMUS
Association DECONSEILLEERisque d'augmentation des concentrations plasmatiques de
dabigatran.
+ TICAGRELOR
A prendre en compteAugmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
+ VERAPAMIL
Précaution d'emploi
Dans l'indication post-chirurgicale : surveillance clinique et adaptation
de la posologie du dabigatran à 150 mg/j en une prise, voire 75 mg/j en
cas d'insuffisance rénale modérée.
Dans l'indication fibrillation auriculaire : surveillance clinique et
adaptation de la posologie du dabigatran à 220 mg/j en deux prises.
Augmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
DACARBAZINE
Voir aussi : cytotoxiques
+ FOTEMUSTINE
Précaution d'emploi
Ne pas utiliser simultanément mais respecter un délai d'une semaine
entre la dernière administration de fotémustine et le premier jour de la
cure de dacarbazine.
Avec la dacarbazine à doses élevées : risque de toxicité
pulmonaire (syndrome de détresse respiratoire aiguë de l'adulte).
DALFOPRISTINE
+ DIHYDROERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ ERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ PIMOZIDE
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
DANAZOL
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation de la posologie de
l’antivitamine K pendant le traitement par le danazol et après son arrêt.
Augmentation du risque hémorragique par effet direct sur la
coagulation et/ou les systèmes fibrinolytiques.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine.
Augmentation des concentrations plasmatiques de carbamazépine,
avec signes de surdosage.
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l’association et
après son arrêt.
Augmentation des concentrations sanguines de ciclosporine par
inhibition de son métabolisme hépatique.
+ INSULINE
Association DECONSEILLEE
Si l'association ne peut être évitée, prévenir le patient et renforcer
l'autosurveillance glycémique. Adapter éventuellement la posologie de
l'insuline pendant le traitement par le danazol et après son arrêt.
Effet diabétogène du danazol.
70
+ SIMVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par diminution du métabolisme de la
simvastatine.
+ SULFAMIDES HYPOGLYCÉMIANTS
Association DECONSEILLEE
Si l'association ne peut être évitée, prévenir le patient et renforcer
l'autosurveillance glycémique. Adapter éventuellement la posologie de
l'antidiabétique pendant le traitement par le danazol et après son arrêt.
Effet diabétogène du danazol.
+ TACROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines du tacrolimus et adaptation de sa
posologie pendant l'association et après son arrêt, avec contrôle de la
fonction rénale.
Augmentation des concentrations sanguines du tacrolimus par
inhibition de son métabolisme hépatique.
DANTROLENE
+ DIHYDROPYRIDINES
Association DECONSEILLEEAvec le dantrolène administré par perfusion : chez l'animal des cas
de fibrillations ventriculaires mortelles sont constamment observés
lors de l'administration de vérapamil et de dantrolène IV.
L'association d'un antagoniste du calcium et de dantrolène est donc
potentiellement dangereuse. Cependant, quelques patients ont
reçu l'association nifédipine et dantrolène sans inconvénient.
+ DILTIAZEM
CONTRE-INDICATIONAvec le dantrolène administré par perfusion : chez l'animal, des cas
de fibrillations ventriculaires mortelles sont constamment observés
lors de l'administration de vérapamil et de dantrolène par voie IV.
L'association d'un antagoniste du calcium et de dantrolène est donc
potentiellement dangereuse. Cependant, quelques patients ont
reçu l'association nifédipine et dantrolène sans inconvénient.
+ VERAPAMIL
CONTRE-INDICATIONAvec le dantrolène administré par perfusion : chez l'animal, des cas
de fibrillations ventriculaires mortelles sont constamment observés
lors de l'administration de vérapamil et de dantrolène par voie IV.
L'association d'un antagoniste du calcium et de dantrolène est donc
potentiellement dangereuse. Cependant, quelques patients ont
reçu l'association nifédipine et dantrolène sans inconvénient.
DAPOXÉTINE
Voir aussi : inhibiteurs sélectifs de la recapture de la sérotonine - médicaments sédatifs
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONRisque de majoration des effets indésirables, notamment à type de
vertiges ou de syncopes.
+ MÉDICAMENTS À L'ORIGINE D'UNE HYPOTENSION ORTHOSTATIQUE
ASDEC - APEC
Association déconseillée
- avec les inhibiteurs de la phosphodiestérase de type 5
A prendre en compte
- avec les autres classes thérapeutiques
Risque de majoration des effets indésirables, notamment à type de
vertiges ou de syncopes.
DAPSONE
Voir aussi : médicaments méthémoglobinisants
+ ZIDOVUDINE
Précaution d'emploi
Contrôle plus fréquent de l'hémogramme.
Augmentation de la toxicité hématologique (addition d'effets de
toxicité médullaire).
DAPTOMYCINE
Voir aussi : médicaments à l'origine d'atteintes musculaires
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Association DECONSEILLEE
Si l’association ne peut être évitée, renforcer la surveillance biologique
(dosage des CPK plus d’une fois par semaine) et surveillance clinique
étroite.
Risque d’addition des effets indésirables (dose-dépendant) à type
de rhabdomyolyse.
71
DARIFENACINE
Voir aussi : antispasmodiques urinaires - médicaments atropiniques
+ METOPROLOL
Précaution d'emploi
Surveillance clinique et réduction de la posologie du métoprolol pendant
le traitement par darifénacine.
Augmentation des concentrations plasmatiques du métoprolol,
avec risque de surdosage, par diminution de son métabolisme
hépatique par la darifénacine.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par darifénacine.
Augmentation des concentrations plasmatiques de propafénone,
avec risque de surdosage, par diminution de son métabolisme
hépatique par la darifénacine.
DAROLUTAMIDE
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques de dalorutamide avec
risque de perte d’efficacité.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de dalorutamide avec
risque de perte d’efficacité.
+ ROSUVASTATINE
Association DECONSEILLEEAugmentation considérable (d’un facteur 5) des concentrations de
rosuvastatine avec risque de rhabdomyolyse et/ou de
néphrotoxicité, par augmentation de sa biodisponibilité.
DARUNAVIR
Voir aussi : inhibiteurs de protéases boostés par ritonavir
+ ETRAVIRINE
Association DECONSEILLEERisque de diminution des concentrations plasmatiques du
darunavir par l’étravirine.
DASABUVIR
+ ETHINYLESTRADIOL
CONTRE-INDICATIONAugmentation de l’hépatotoxicité.
+ GEMFIBROZIL
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques du
dasabuvir par le gemfibrozil.
+ INDUCTEURS ENZYMATIQUES
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques du
dasabuvir par l’inducteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques du
dasabuvir par le millepertuis.
+ MITOTANE
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques du
dasabuvir par le mitotane.
DEFERASIROX
+ ACIDE ACETYLSALICYLIQUE
A prendre en compte
A prendre en compte :
- Pour des doses anti-inflammatoires d'acide acétylsalicylique ( 1g par
prise et/ou 3g par jour)
- Pour des doses antalgiques ou antipyrétiques d'acide acétylsalicylique
( 500 mg par prise et/ou <3g par jour) et ( 500 mg par prise et/ou <3g
par jour)
Majoration du risque ulcérogène et hémorragique digestif.
72
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
A prendre en compteMajoration du risque ulcérogène et hémorragique digestif.
+ ANTIVITAMINES K
A prendre en compteMajoration du risque ulcérogène et hémorragique digestif.
+ BUSULFAN
A prendre en compteRisque d’augmentation de la toxicité du busulfan par diminution de
sa clairance par le déférasirox.
+ DÉFÉRIPRONE
CONTRE-INDICATIONRisque d'hyperchélation.
+ DÉFÉROXAMINE
CONTRE-INDICATIONRisque d'hyperchélation.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveiller la ferritinémie pendant et après le traitement par l’inducteur
enzymatique. Si besoin, adaptation de la posologie de déférasirox.
Risque de diminution des concentrations plasmatiques de
déférasirox.
+ PACLITAXEL
Précaution d'emploi
Surveillance clinique et biologique étroite.
Risque d’augmentation des concentrations plasmatiques du
paclitaxel par inhibition de son métabolisme hépatique par le
deferasirox.
+ REPAGLINIDE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite.
Risque d’augmentation des concentrations plasmatique de
répaglinide, par inhibition de son métabolisme hépatique par le
deferasirox.
+ RIFAMPICINE
Précaution d'emploi
Surveiller la ferritinémie pendant et après le traitement par l’inducteur
enzymatique. Si besoin, adaptation de la posologie de déférasirox.
Risque de diminution des concentrations plasmatiques de
déférasirox.
+ SELEXIPAG
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
DÉFÉRIPRONE
+ ACIDE ASCORBIQUE
Précaution d'emploiPar extrapolation à partir de l’interaction avec la déféroxamine :
avec l’acide ascorbique à fortes doses et par voie IV, risque
d’anomalies de la fonction cardiaque, voire insuffisance cardiaque
aiguë (en général réversible à l’arrêt de la vitamine C).
+ DEFERASIROX
CONTRE-INDICATIONRisque d'hyperchélation.
DÉFÉROXAMINE
+ ACIDE ASCORBIQUE
Précaution d'emploi
En cas d'hémochromatose, ne donner de la vitamine C qu'après avoir
commencé le traitement par la déféroxamine. Surveiller la fonction
cardiaque en cas d'association.
Avec l'acide ascorbique à fortes doses et par voie IV : anomalies de
la fonction cardiaque, voire insuffisance cardiaque aiguë (en
général réversible à l'arrêt de la vitamine C).
+ DEFERASIROX
CONTRE-INDICATIONRisque d'hyperchélation.
73
DÉFIBROTIDE
+ ANTIAGRÉGANTS PLAQUETTAIRES
Association DECONSEILLEERisque hémorragique accru.
+ ANTICOAGULANTS ORAUX
Association DECONSEILLEERisque hémorragique accru.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ HÉPARINES
Association DECONSEILLEERisque hémorragique accru.
+ THROMBOLYTIQUES
CONTRE-INDICATIONRisque hémorragique accru.
DÉLAMANID
+ INDUCTEURS ENZYMATIQUES PUISSANTS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de delamanid par
augmentation de son métabolisme hépatique par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
+ RIFAMPICINE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de delamanid par
augmentation de son métabolisme hépatique par l’inducteur.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication:
- avec citalopram, dompéridone, escitalopram, hydroxyzine et
pipéraquine
Associations déconseillées
- avec les autres susbtances susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
DÉRIVÉS DE L'ACIDE AMINOSALICYLIQUE (ASA)
(mesalazine, olsalazine, p a s sodique, sulfasalazine)
+ ANTIPURINES
A prendre en compteRisque de majoration de l'effet myélosuppresseur de
l'immunomodulateur par inhibition de son métabolisme hépatique
par le dérivé de l'ASA, notamment chez les sujets présentant un
déficit partiel en thiopurine méthyltransférase (TPMT).
DÉRIVÉS NITRÉS ET APPARENTÉS
(dinitrate d'isosorbide, isosorbide, molsidomine, nicorandil, trinitrine)
+ INHIBITEURS DE LA PHOSPHODIESTERASE DE TYPE 5
CONTRE-INDICATIONRisque d'hypotension importante (effet synergique) pouvant
aggraver l'état d'ischémie myocardique et provoquer notamment un
accident coronarien aigu.
+ RIOCIGUAT
CONTRE-INDICATIONRisque d'hypotension importante (effet synergique).
74
DESIPRAMINE
+ BUPROPION
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
désipramine pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la désipramine
par diminution de son métabolisme hépatique par le bupropion.
DEXAMETHASONE
Voir aussi : corticoïdes - corticoïdes (voie intra-articulaire) - corticoïdes métabolisés, notamment inhalés - glucocorticoïdes (sauf hydrocortisone) - glucocorticoïdes par
voie intra-articulaire et métabolisés - hypokaliémiants - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ PRAZIQUANTEL
Précaution d'emploi
Décaler l'administration des deux médicaments d'au moins une
semaine.
Diminution des concentrations plasmatiques du praziquantel, avec
risque d'échec du traitement, par augmentation du métabolisme
hépatique du praziquantel par la dexaméthasone.
+ RILPIVIRINE
CONTRE-INDICATIONAvec la dexaméthasone par voie systémique (sauf en cas de prise
unique), risque de diminution des concentrations plasmatiques de
rilpivirine par augmentation de son métabolisme hépatique par la
dexamethasone.
DEXTRAN
+ HÉPARINES (DOSES CURATIVES ET/OU SUJET ÂGÉ)
Association DECONSEILLEEAugmentation du risque hémorragique (inhibition de la fonction
plaquettaire par le dextran 40).
DEXTROMETHORPHANE
Voir aussi : antitussifs morphine-like - morphiniques - médicaments sédatifs
+ CINACALCET
CONTRE-INDICATIONAugmentation très importante des concentrations plasmatiques de
dextrométhorphane avec risque de surdosage, par diminution de
son métabolisme hépatique par le cinacalcet.
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
Association DECONSEILLEERisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
DIAZEPAM
Voir aussi : benzodiazépines et apparentés - médicaments sédatifs
+ BUSPIRONE
A prendre en compteRisque de majoration des effets indésirables de la buspirone.
+ CIMETIDINE
Précaution d'emploi
Avertir les patients de l'augmentation du risque en cas de conduite
automobile ou d'utilisation de machines.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : risque accru de somnolence.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne.
Variations imprévisibles : les concentrations plasmatiques de
phénytoïne peuvent augmenter, avec signes de surdosage, mais
aussi diminuer ou rester stables.
+ STIRIPENTOL
Précaution d'emploi
Surveillance clinique et dosage plasmatique, lorsque cela est possible,
de l'anticonvulsivant associé au stiripentol et éventuelle adaptation
posologique de l'anticonvulsivant associé.
Augmentation des concentrations plasmatiques du diazépam, avec
risque de surdosage, par inhibition de son métabolisme hépatique.
DIDANOSINE
+ ALLOPURINOL
Association DECONSEILLEEAugmentation des concentrations plasmatiques de didanosine et
de ses effets indésirables.
75
+ GANCICLOVIR
Association DECONSEILLEERisque d'augmentation des effets indésirables de la didanosine, et
notamment la toxicité mitochondriale, par augmentation importante
de ses concentrations. De plus risque de diminution de l'efficacité
du ganciclovir par diminution de ses concentrations, si les deux
médicaments sont ingérés à moins de 2 heures d'intervalle.
+ PENTAMIDINE
Précaution d'emploi
Surveillance de l'amylasémie. Ne pas associer si l'amylasémie est à la
limite supérieure de la normale.
Risque majoré de survenue de pancréatite par addition d'effets
indésirables.
+ RIBAVIRINE
Association DECONSEILLEERisque de majoration de la toxicité mitochondriale de la didanosine
par augmentation de son métabolite actif.
+ TENOFOVIR DISOPROXIL
Association DECONSEILLEERisque d'échec du traitement antirétroviral, voire émergence de
résistances. De plus, majoration du risque de la toxicité
mitochondriale de la didanosine.
+ THALIDOMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
DIGOXINE
Voir aussi : bradycardisants - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ AMIODARONE
Précaution d'emploi
Surveillance clinique, ECG et, s'il y a lieu, contrôle de la digoxinémie et
adaptation de la posologie de la digoxine.
Dépression de l'automatisme (bradycardie excessive) et troubles
de la conduction auriculo-ventriculaire. De plus, augmentation de la
digoxinémie par diminution de la clairance de la digoxine.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
A prendre en compteTroubles de l’automatisme (bradycardie, arrêt sinusal) et troubles
de la conduction sino-auriculaire et auriculo-ventriculaire.
+ CALCIUM
CI - PE
Contre-indication :
- avec les sels de calcium IV, hormis supplémentation parentérale.
Précaution d'emploi :
- avec les sels de calcium par voie orale.
Surveillance clinique et, s'il y a lieu, contrôle de l'ECG et de la calcémie.
Risque de troubles du rythme graves, voire mortels avec les sels
de calcium administrés par voie IV.
+ CARBAMAZEPINE
Précaution d'emploi
Prudence dans l'interprétation des concentrations plasmatiques.
Augmentation des concentrations plasmatiques de carbamazépine
et diminution de la digoxinémie.
+ DRONEDARONE
Association DECONSEILLEE
Réduire de moitié les doses de digoxine.
Dépression de l'automatisme (bradycardie excessive) et troubles
de la conduction auriculo-ventriculaire. En outre, augmentation de
la digoxinémie par diminution du métabolisme de la digoxine.
Surveillance clinique et ECG.
+ GLÉCAPRÉVIR + PIBRENTASVIR
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par glécaprévir/ pibrentasvir.
Augmentation des concentrations plasmatiques de la digoxine par
la bithérapie.
+ HYDROQUINIDINE
Précaution d'emploi
Surveillance clinique et ECG. En cas de réponse inattendue, contrôler
la digoxinémie et adapter la posologie.
Augmentation de la digoxinémie par diminution de la clairance
rénale de la digoxine. De plus, troubles de l'automatisme
(bradycardie excessive et troubles de la conduction auriculo-
ventriculaire).
+ HYPOKALIÉMIANTS
Précaution d'emploi
Corriger auparavant toute hypokaliémie et réaliser une surveillance
clinique, électrolytique et électrocardiographique.
Hypokaliémie favorisant les effets toxiques des digitaliques.
76
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique et, s’il y a lieu, de l’ECG et de la digoxinémie, avec
adaptation éventuelle de la posologie de digoxine.
Augmentation de la digoxinémie, plus marquée pour la voie
intraveineuse, par augmentation de l’absorption de la digoxine ou
diminution de sa clairance rénale.
+ ITRACONAZOLE
Précaution d'emploi
Surveillance clinique et, s'il y a lieu, de l'ECG et de la digoxinémie avec
adaptation de la posologie de la digoxine pendant le traitement par
l'itraconazole et après son arrêt.
Augmentation de la digoxinémie avec nausées, vomissements,
troubles du rythme.
+ MACROLIDES (SAUF SPIRAMYCINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par le macrolide et après son arrêt.
Augmentation de la digoxinémie par augmentation de son
absorption.
+ MIDODRINE
Association DECONSEILLEE
Si cette association ne peut être évitée, renforcer la surveillance
clinique et ECG.
Troubles de l'automatisme (majoration de l'effet bradycardisant de
la midodrine) et troubles de la conduction auriculo-ventriculaire.
+ MILLEPERTUIS
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler les concentrations plasmatiques (ou
l'efficacité) de la digoxine avant puis après l'arrêt du millepertuis.
Diminution de la digoxinémie, en raison de l'effet inducteur du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet, dont les conséquences peuvent être éventuellement graves
(décompensation d'une insuffisance cardiaque).
+ OMEPRAZOLE
Précaution d'emploi
Surveillance clinique, ECG et de la digoxinémie, particulièrement chez
le sujet âgé.
Augmentation modérée de la digoxinémie par majoration de son
absorption par l'oméprazole.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
digoxine par augmentation de son absorption intestinale par le
ponatinib.
+ POSACONAZOLE
Précaution d'emploi
Surveillance clinique et, s'il y a lieu, de l'ECG et de la digoxinémie, avec
adaptation de la posologie de la digoxine pendant le traitement par le
posaconazole et après son arrêt.
Augmentation de la digoxinémie avec nausées, vomissements,
troubles du rythme.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par propafénone et après son arrêt.
Risque d’augmentation de la digoxinémie, notamment chez le sujet
âgé.
+ QUINIDINE
Précaution d'emploi
Surveillance clinique et ECG. En cas de réponse inattendue, contrôler
la digoxinémie et adapter la posologie.
Augmentation de la digoxinémie par diminution de la clairance
rénale de la digoxine. De plus, troubles de l'automatisme
(bradycardie excessive et troubles de la conduction auriculo-
ventriculaire).
+ QUININE
Précaution d'emploi
Surveillance clinique et ECG, si besoin, avec adaptation éventuelle des
doses de digoxine.
Augmentation modérée de la digoxinémie.
+ RANOLAZINE
Précaution d'emploi
Surveillance clinique, biologique et éventuellement ECG. Adaptation de
la posologie de la digoxine, si besoin.
Augmentation de la digoxinémie.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et ECG.
Diminution modeste des concentrations de digoxine.
+ ROLAPITANT
Précaution d'emploi
Surveillance clinique et ECG pendant le traitement par le rolapitant et
après son arrêt.
Augmentation de la digoxinémie par majoration de son absorption.
77
+ SUCRALFATE
Précaution d'emploi
Prendre le sucralfate à distance de la digoxine (plus de 2 heures, si
possible).
Diminution de l'absorption digestive de la digoxine.
+ SULFASALAZINE
Précaution d'emploi
Surveillance clinique, ECG et, éventuellement, de la digoxinémie. S'il y
a lieu, adaptation de la posologie de la digoxine pendant le traitement
par la sulfasalazine et après son arrêt.
Diminution de la digoxinémie pouvant atteindre 50 %.
+ TELITHROMYCINE
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par la télithromycine et après son arrêt.
Augmentation de la digoxinémie par augmentation de son
absorption.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique, ECG et, éventuellement, contrôle de la
digoxinémie. S'il y a lieu, adaptation de la posologie de la digoxine
pendant le traitement par le vérapamil et après son arrêt.
Bradycardie excessive et bloc auriculo-ventriculaire par majoration
des effets de la digoxine sur l'automatisme et la conduction et par
diminution de l'élimination rénale et extrarénale de la digoxine.
DIHYDROERGOTAMINE
Voir aussi : alcaloïdes de l'ergot de seigle vasoconstricteurs - substrats à risque du CYP3A4
+ DALFOPRISTINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ DILTIAZEM
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ EFAVIRENZ
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ MACROLIDES (SAUF SPIRAMYCINE)
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition de
l’élimination hépatique de l'alcaloïde de l’ergot de seigle).
+ QUINUPRISTINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ STIRIPENTOL
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition de
l’élimination hépatique de l'alcaloïde de l’ergot de seigle).
+ TRICLABENDAZOLE
CONTRE-INDICATION
Respecter un délai de 24 heures entre l’arrêt du triclabendazole et la
prise du médicament dérivé de l’ergot, et inversement.
Ergotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l’alcaloïde de l’ergot de seigle).
DIHYDROPYRIDINES
(amlodipine, clévidipine, felodipine, isradipine, lacidipine, lercanidipine, manidipine, nicardipine, nifedipine, nimodipine, nitrendipine)
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
A prendre en compteHypotension, défaillance cardiaque chez les patients en
insuffisance cardiaque latente ou non contrôlée (addition des effets
inotropes négatifs). Le bêta-bloquant peut par ailleurs minimiser la
réaction sympathique réflexe mise en jeu en cas de répercussion
hémodynamique excessive.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
A prendre en compteHypotension, défaillance cardiaque chez les malades en
insuffisance cardiaque latente ou non contrôlée (effet inotrope
négatif in vitro des dihydropyridines plus ou moins marqué et
susceptibles de s'additionner aux effets inotropes négatifs des bêta-
bloquants). La présence d'un traitement bêta-bloquant peut par
ailleurs minimiser la réaction sympathique réflexe mise en jeu en
cas de répercussion hémodynamique excessive.
78
+ DANTROLENE
Association DECONSEILLEEAvec le dantrolène administré par perfusion : chez l'animal des cas
de fibrillations ventriculaires mortelles sont constamment observés
lors de l'administration de vérapamil et de dantrolène IV.
L'association d'un antagoniste du calcium et de dantrolène est donc
potentiellement dangereuse. Cependant, quelques patients ont
reçu l'association nifédipine et dantrolène sans inconvénient.
DILTIAZEM
Voir aussi : antagonistes des canaux calciques - antiarythmiques - antihypertenseurs sauf alpha-bloquants - bradycardisants - médicaments abaissant la pression
artérielle
+ ALFENTANIL
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par le diltiazem.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
+ AMIODARONE
ASDEC - PE
Association déconseillée avec :
- le diltiazem IV
Si l'association ne peut être évitée, surveillance clinique et ECG continu.
Précaution d'emploi avec :
- le diltiazem per os
Surveillance clinique et ECG.
Pour diltiazem voie injectable : risque de bradycardie et de bloc
auriculo-ventriculaire
Pour diltiazem per os : risque de bradycardie ou de bloc auriculo-
ventriculaire, notamment chez les personnes âgées.
+ ANTIHYPERTENSEURS CENTRAUX
A prendre en compteTroubles de l'automatisme (troubles de la conduction auriculo-
ventriculaire par addition des effets négatifs sur la conduction).
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Association DECONSEILLEE
Une telle association ne doit se faire que sous surveillance clinique et
ECG étroite, en particulier chez le sujet âgé ou en début de traitement.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
troubles de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Association DECONSEILLEEEffet inotrope négatif avec risque de décompensation de
l’insuffisance cardiaque, troubles de l'automatisme (bradycardie,
arrêt sinusal) et troubles de la conduction sino-auriculaire et
auriculo-ventriculaire.
+ BUSPIRONE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buspirone si
nécessaire.
Augmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique par le diltiazem, avec
augmentation de ses effets indésirables.
+ DANTROLENE
CONTRE-INDICATIONAvec le dantrolène administré par perfusion : chez l'animal, des cas
de fibrillations ventriculaires mortelles sont constamment observés
lors de l'administration de vérapamil et de dantrolène par voie IV.
L'association d'un antagoniste du calcium et de dantrolène est donc
potentiellement dangereuse. Cependant, quelques patients ont
reçu l'association nifédipine et dantrolène sans inconvénient.
+ DIHYDROERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ DRONEDARONE
Précaution d'emploi
Débuter le traitement par l’antagoniste calcique aux posologies
minimales recommandées, et ajuster les doses en fonction de l’ECG.
Risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez le sujet âgé. Par ailleurs, légère augmentation des
concentrations de dronédarone par diminution de son métabolisme
par l’antagoniste des canaux calciques.
+ ERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
79
+ ESMOLOL
ASDEC - PE
Association déconseillée :
- en cas d'altération de la fonction ventriculaire gauche.
Précaution d'emploi :
- si la fonction ventriculaire gauche est normale.
Surveillance clinique et ECG.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
troubles de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d'augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le diltiazem.
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par diminution de son métabolisme.
+ IVABRADINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l’ivabradine et
de ses effets indésirables, notamment cardiaques (inhibition de son
métabolisme hépatique par le diltiazem), qui s’ajoutent aux effets
bradycardisants de ces substances.
+ LOMITAPIDE
CONTRE-INDICATIONAugmentation des concentrations de lomitapide, avec risque
d’hépatotoxicité.
+ MIDAZOLAM
Précaution d'emploi
Surveillance clinique et réduction de la posologie pendant le traitement
par le diltiazem.
Augmentation des concentrations plasmatiques de midazolam par
diminution de son métabolisme hépatique, avec majoration de la
sédation.
+ NALOXEGOL
Précaution d'emploi
Adaptation posologique pendant l’association.
Augmentation des concentrations plasmatiques de naloxegol par le
diltiazem.
+ NIFEDIPINE
CONTRE-INDICATIONAugmentation importantes des concentrations de nifédipine par
diminution de son métabolisme hépatique par le diltiazem, avec
risque d'hypotension sévère.
+ OLAPARIB
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par le
diltiazem.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SIMVASTATINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/jour de simvastatine. Si
l'objectif thérapeutique n'est pas atteint à cette posologie, utiliser une
autre statine non concernée par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ TAMSULOSINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la tamsulosine
pensant le traitement par l’inhibiteur enzymatique et après son arrêt, le
cas échéant.
Risque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
+ TICAGRELOR
A prendre en compteRisque d’augmentation des concentrations plasmatiques de
ticagrelor par diminution de son métabolisme hépatique.
+ TOLVAPTAN
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
80
+ VÉNÉTOCLAX
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment hématologique,
et adaptation de la posologie du vénétoclax.
Risque d’augmentation des effets indésirables du vénétoclax par
diminution de son métabolisme hépatique.
DIMÉTHYLE ( FUMARATE DE)
+ VACCINS VIVANTS ATTÉNUÉS
A prendre en comptePossible augmentation du risque infectieux.
DIPROPHYLLINE
+ PROBENECIDE
Précaution d'emploi
Réduire la posologie de diprophylline pendant le traitement par le
probénécide.
Risque de surdosage par augmentation des concentrations
plasmatiques de diprophylline (inhibition de sa sécrétion tubulaire
rénale).
DIPYRIDAMOLE
+ THÉINE
Précaution d'emploi
Eviter la consommation de produits à base de théine dans les 24
heures qui précèdent une imagerie myocardique avec le dipyridamole.
Avec le dipyridamole par voie injectable : réduction de l’effet
vasodilatateur du dipyridamole par la théine.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
A prendre en compteAvec le dipyridamole par voie injectable : majoration de l'effet
antihypertenseur.
+ CAFEINE
Précaution d'emploi
Interrompre un traitement à base de caféine au moins 5 jours avant une
imagerie myocardique avec le dipyridamole et éviter la consommation
de café, thé, chocolat ou cola dans les 24 heures qui précèdent le test.
Avec le dipyridamole par voie injectable : réduction de l’effet
vasodilatateur du dipyridamole par la caféine.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Interrompre un traitement par théophylline au moins 5 jours avant une
imagerie myocardique avec le dipyridamole.
Avec le dipyridamole par voie injectable : réduction de l’effet
vasodilatateur du dipyridamole par la théophylline.
DISOPYRAMIDE
Voir aussi : antiarythmiques - antiarythmiques classe Ia - bradycardisants - médicaments atropiniques - substances susceptibles de donner des torsades de pointes -
torsadogènes (sauf arsénieux, antiparasitaires, neuroleptiques, méthadone...)
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Surveillance clinique et éventuellement adaptation de la posologie du
disopyramide pendant l’association et 1 à 2 semaines après l’arrêt de
l’inducteur.
Risque de diminution des concentrations du disopyramide par
l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
disopyramide.
Risque d’augmentation des effets indésirables du disopyramide par
diminution de son métabolisme.
+ JOSAMYCINE
Précaution d'emploi
Surveillance clinique, biologique et électrocardiographique régulière.
Risque de majoration des effets indésirables du disopyramide :
hypoglycémies sévères, allongement de l’intervalle QT et troubles
du rythme ventriculaire graves, notamment à type de torsades de
pointes.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques de
disopyramide et de ses effets indésirables.
DISULFIRAME
Voir aussi : antabuse (réaction)
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation de la posologie de
l'antivitamine K pendant le traitement par le disulfirame et 8 jours après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
81
+ COCAINE
A prendre en compteAugmentation des concentrations de cocaïne par diminution de son
métabolisme par le disulfirame, avec risque majoré de survenue de
torsades de pointes.
+ ISONIAZIDE
Association DECONSEILLEETroubles du comportement et de la coordination.
+ METRONIDAZOLE
Association DECONSEILLEERisque d’épisodes de psychose aiguë ou d’état confusionnel,
réversibles à l’arrêt de l’association.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Association DECONSEILLEE
Si elle ne peut être évitée, contrôle clinique et des concentrations
plasmatiques de phénytoïne pendant le traitement par le disulfirame et
après son arrêt.
Augmentation importante et rapide des concentrations
plasmatiques de phénytoïne avec signes toxiques (inhibition de son
métabolisme).
DIURÉTIQUES
(altizide, amiloride, bendroflumethiazide, bumetanide, canrenoate de potassium, chlortalidone, cicletanine, clopamide, eplerenone, furosemide, hydrochlorothiazide,
indapamide, methyclothiazide, piretanide, spironolactone, triamterene)
+ ACIDE ACETYLSALICYLIQUE
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Pour des doses anti-inflammatoires d'acide acétylsalicylique (>= 1g
par prise et/ou >= 3g par jour) ou pour des doses antalgiques ou
antipyrétiques (>= 500 mg par prise et/ou < 3g par jour) :
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
avec une fonction rénale altérée), par diminution de la filtration
glomérulaire secondaire à une diminution de la synthèse des
prostaglandines rénales. Par ailleurs, réduction de l'effet
antihypertenseur.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l'association.
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Ces effets sont
généralement réversibles. Par ailleurs, réduction de l’effet
antihypertenseur.
+ PRODUITS DE CONTRASTE IODÉS
Précaution d'emploi
Réhydratation avant administration du produit iodé.
En cas de déshydratation provoquée par les diurétiques, risque
majoré d'insuffisance rénale fonctionnelle aiguë, en particulier lors
d'utilisation de doses importantes de produits de contraste iodés.
DIURÉTIQUES DE L'ANSE
(bumetanide, furosemide, piretanide)
+ AMINOSIDES
Précaution d'emploi
Association possible sous contrôle de l'état d'hydratation, des fonctions
rénale et cochléovestibulaire, et éventuellement, des concentrations
plasmatiques de l'aminoside.
Augmentation des risques néphrotoxiques et ototoxiques de
l'aminoside (insuffisance rénale fonctionnelle liée à la
déshydratation entraînée par le diurétique).
+ LITHIUM
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance stricte de la lithémie et
adaptation de la posologie du lithium.
Augmentation de la lithémie avec signes de surdosage en lithium,
comme lors d’un régime désodé (diminution de l’excrétion urinaire
du lithium).
+ METFORMINE
Précaution d'emploi
Ne pas utiliser la metformine lorsque la créatininémie dépasse 15 mg/l
(135 μmol/l) chez l'homme, et 12 mg/l (110 μmol/l) chez la femme.
Acidose lactique due à la metformine, déclenchée par une
éventuelle insuffisance rénale fonctionnelle, liée aux diurétiques de
l'anse.
+ ORGANOPLATINES
A prendre en compteRisque d’addition des effets ototoxiques et/ou néphrotoxiques.
DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
(amiloride, canrenoate de potassium, eplerenone, spironolactone, triamterene)
+ AUTRES DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
CONTRE-INDICATION
Contre-indiqué sauf s'il existe une hypokaliémie.
Hyperkaliémie potentiellement létale, notamment chez l'insuffisant
rénal (addition des effets hyperkaliémiants).
82
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
ASDEC - PE
Association déconseillée :
- si l'association est justifiée, contrôle strict de la kaliémie et de la
fonction rénale.
Précaution d'emploi :
- pour la spironolactone à des doses comprises entre 12,5 mg et 50
mg/jour, et pour l’éplérénone utilisées dans le traitement de
l'insuffisance cardiaque, ainsi qu'en cas d'hypokaliémie : contrôle strict
de la kaliémie et de la fonction rénale.
Risque d'hyperkaliémie (potentiellement létale) surtout en cas
d'insuffisance rénale (addition des effets hyperkaliémiants).
+ CICLOSPORINE
Association DECONSEILLEEHyperkaliémie potentiellement létale, surtout lors d'une insuffisance
rénale (addition des effets hyperkaliémiants).
+ DIURÉTIQUES HYPOKALIÉMIANTS
Précaution d'emploi
Surveiller la kaliémie, éventuellement l'ECG et, s'il y a lieu, reconsidérer
le traitement.
L'association rationnelle, utile pour certains patients, n'exclut pas la
survenue d'hypokaliémie ou, en particulier chez l'insuffisant rénal et
le diabétique, d'hyperkaliémie.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
ASDEC - PE
Association déconseillée :
- si l'association est justifiée, contrôle strict de la kaliémie et de la
fonction rénale.
Précaution d'emploi :
- pour la spironolactone à des doses comprises entre 12,5 mg et 50
mg/jour, et pour l’éplérénone utilisées dans le traitement de
l'insuffisance cardiaque, ainsi qu'en cas d'hypokaliémie : contrôle strict
de la kaliémie et de la fonction rénale.
Risque d'hyperkaliémie (potentiellement létale) surtout en cas
d'insuffisance rénale (addition des effets hyperkaliémiants).
+ LITHIUM
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Augmentation de la lithémie avec signes de surdosage en lithium,
comme lors d’un régime désodé (diminution de l’excrétion urinaire
du lithium).
+ POTASSIUM
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénal (addition
des effets hyperkaliémiants).
+ TACROLIMUS
Association DECONSEILLEEHyperkaliémie potentiellement létale, surtout lors d'une insuffisance
rénale (addition des effets hyperkaliémiants).
DIURÉTIQUES HYPOKALIÉMIANTS
(altizide, bendroflumethiazide, bumetanide, chlortalidone, cicletanine, clopamide, furosemide, hydrochlorothiazide, indapamide, methyclothiazide, piretanide)
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
Précaution d'emploi
Dans l'hypertension artérielle, lorsqu'un traitement diurétique préalable
a pu entraîner une déplétion hydrosodée, il faut :
- soit arrêter le diurétique avant de débuter le traitement par
l'antagoniste de l'angiotensine II, et réintroduire un diurétique
hypokaliémiant si nécessaire ultérieurement ;
- soit administrer des doses initiales réduites d'antagoniste de
l'angiotensine II et augmenter progressivement la posologie.
Dans tous les cas : surveiller la fonction rénale (créatininémie) dans les
premières semaines du traitement par l'antagoniste de l'angiotensine II.
Risque d'hypotension artérielle brutale et/ou d'insuffisance rénale
aiguë lors de l'instauration ou de l'augmentation de la posologie
d'un traitement par un antagoniste de l'angiotensine II en cas de
déplétion hydrosodée préexistante.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et biologique. Si possible, utiliser une autre classe
de diurétiques.
Risque d'hyponatrémie symptomatique.
+ CICLOSPORINE
A prendre en compteRisque d'augmentation de la créatininémie sans modification des
concentrations sanguines de ciclosporine, même en l'absence de
déplétion hydrosodée. Egalement, risque d'hyperuricémie et de
complications comme la goutte.
+ DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
Précaution d'emploi
Surveiller la kaliémie, éventuellement l'ECG et, s'il y a lieu, reconsidérer
le traitement.
L'association rationnelle, utile pour certains patients, n'exclut pas la
survenue d'hypokaliémie ou, en particulier chez l'insuffisant rénal et
le diabétique, d'hyperkaliémie.
83
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Précaution d'emploi
Dans l'hypertension artérielle, lorsqu'un traitement diurétique préalable
a pu entraîner une déplétion hydrosodée, il faut :
- soit arrêter le diurétique avant de débuter le traitement par l'IEC, et
réintroduire un diurétique hypokaliémiant si nécessaire ultérieurement ;
- soit administrer des doses initiales réduites d'IEC et augmenter
progressivement la posologie.
Dans l'insuffisance cardiaque congestive traitée par diurétiques,
commencer par une dose très faible d'IEC, éventuellement après
réduction de la dose du diurétique hypokaliémient associé.
Dans tous les cas : surveiller la fonction rénale (créatininémie) dans les
premières semaines du traitement par l'IEC.
Risque d'hypotension artérielle brutale et/ou d'insuffisance rénale
aiguë lors de l'instauration ou de l'augmentation de la posologie
d'un traitement par un inhibiteur de l'enzyme de conversion en cas
de déplétion hydrosodée préexistante.
DIURÉTIQUES THIAZIDIQUES ET APPARENTÉS
(altizide, bendroflumethiazide, chlortalidone, cicletanine, clopamide, hydrochlorothiazide, indapamide, methyclothiazide)
+ CALCIUM
A prendre en compteRisque d'hypercalcémie par diminution de l'élimination urinaire du
calcium.
+ LITHIUM
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance stricte de la lithémie et
adaptation de la posologie du lithium.
Augmentation de la lithémie avec signes de surdosage en lithium,
comme lors d’un régime désodé (diminution de l’excrétion urinaire
du lithium).
DOCETAXEL
Voir aussi : cytotoxiques - substrats à risque du CYP3A4
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
docétaxel.
Risque de majoration des effets indésirables du docétaxel par
diminution de son métabolisme hépatique par l’amiodarone
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations du
docétaxel, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ DRONEDARONE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
docétaxel pendant le traitement par l’inhibiteur enzymatique.
Risque de majoration de la toxicité du docétaxel par diminution de
son métabolisme.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
docétaxel pendant le traitement par l’inhibiteur enzymatique.
Risque de majoration des effets indésirables dose-dépendants du
docétaxel par inhibition de son métabolisme par l’inhibiteur
enzymatique.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de moindre efficacité du taxane par augmentation de son
métabolisme par le millepertuis.
DOLUTÉGRAVIR
Voir aussi : inhibiteurs d'intégrase - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ INDUCTEURS ENZYMATIQUES
ASDEC - PE
Association déconseillée :
- en cas de résistance à la classe des inhibiteurs d'intégrase
Précaution d'emploi :
- en l'absence de résistance à la classe des inhibiteurs d'intégrase
Adaptation de la posologie de dolutégravir à 50 mg 2 fois par jour
pendant l’association et une semaine après son arrêt.
Diminution des concentrations plasmatiques de dolutégravir par
augmentation de son métabolisme par l’inducteur.
84
+ METFORMINE
Précaution d'emploi
Chez le patient avec une insuffisance rénale modérée, surveillance
clinique et éventuelle réduction supplémentaire de la posologie de
metformine.
Augmentation moyenne de moins de deux fois des concentrations
plasmatiques de metformine.
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
dolutégravir par augmentation de son métabolisme par le
millepertuis.
DOMPERIDONE
Voir aussi : substances susceptibles de donner des torsades de pointes - torsadogènes (sauf arsénieux, antiparasitaires, neuroleptiques, méthadone...)
+ FLUCONAZOLE
CONTRE-INDICATIONRisque de troubles du rythme ventriculaire, notamment de torsades
de pointes.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de dompéridone
par diminution de son métabolisme hépatique par l’inhibiteur.
DOPAMINERGIQUES
(amantadine, apomorphine, bromocriptine, cabergoline, entacapone, lisuride, piribedil, pramipexole, quinagolide, rasagiline, ropinirole, rotigotine, selegiline, tolcapone)
+ NEUROLEPTIQUES ANTIÉMÉTIQUES
CONTRE-INDICATION
Utiliser un antiémétique dénué d'effets extrapyramidaux.
Antagonisme réciproque entre le dopaminergique et le
neuroleptique.
+ TETRABENAZINE
Association DECONSEILLEEAntagonisme réciproque entre le dopaminergique et la
tétrabénazine.
DOPAMINERGIQUES, HORS PARKINSON
(cabergoline, quinagolide)
+ NEUROLEPTIQUES ANTIPSYCHOTIQUES (SAUF CLOZAPINE)
CONTRE-INDICATIONAntagonisme réciproque de l'agoniste dopaminergique et des
neuroleptiques.
DOXORUBICINE
Voir aussi : cytotoxiques
+ VERAPAMIL
A prendre en compteRisque de majoration de la toxicité de la doxorubicine par
augmentation de ses concentrations plasmatiques.
DOXYCYCLINE
Voir aussi : cyclines - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ INDUCTEURS ENZYMATIQUES PUISSANTS
A prendre en compteRisque de diminution importante des concentrations de doxycycline.
+ RIFAMPICINE
A prendre en compteRisque de diminution importante des concentrations de doxycycline.
DRONEDARONE
Voir aussi : antiarythmiques - bradycardisants - substances susceptibles de donner des torsades de pointes - torsadogènes (sauf arsénieux, antiparasitaires,
neuroleptiques, méthadone...)
+ DABIGATRAN
CONTRE-INDICATIONDoublement des concentrations plasmatiques de dabigatran, avec
majoration du risque de saignement.
85
+ DIGOXINE
Association DECONSEILLEE
Réduire de moitié les doses de digoxine.
Dépression de l'automatisme (bradycardie excessive) et troubles
de la conduction auriculo-ventriculaire. En outre, augmentation de
la digoxinémie par diminution du métabolisme de la digoxine.
Surveillance clinique et ECG.
+ DILTIAZEM
Précaution d'emploi
Débuter le traitement par l’antagoniste calcique aux posologies
minimales recommandées, et ajuster les doses en fonction de l’ECG.
Risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez le sujet âgé. Par ailleurs, légère augmentation des
concentrations de dronédarone par diminution de son métabolisme
par l’antagoniste des canaux calciques.
+ DOCETAXEL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
docétaxel pendant le traitement par l’inhibiteur enzymatique.
Risque de majoration de la toxicité du docétaxel par diminution de
son métabolisme.
+ ÉDOXABAN
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
+ FIDAXOMICINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par la dronédarone.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEEAugmentation importante des concentrations sanguines de
l’immunosuppresseur par diminution de son métabolisme.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution importante des concentrations de dronédarone par
augmentation de son métabolisme, sans modification notable du
métabolite actif.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation importante des concentrations de dronédarone par
diminution de son métabolisme.
+ MILLEPERTUIS
Association DECONSEILLEEDiminution importante des concentrations de dronédarone par
augmentation de son métabolisme, sans modification notable du
métabolite actif.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations de dronédarone par inhibition de
son métabolisme par le pamplemousse.
+ QUINIDINE
Précaution d'emploi
Débuter le traitement par la quinidine aux posologies minimales
recommandées, et ajuster les doses en fonction de l’ECG.
Risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez le sujet âgé. Par ailleurs, légère augmentation des
concentrations de dronédarone par diminution de son métabolisme
par la quinidine.
+ RIFAMPICINE
Association DECONSEILLEEDiminution importante des concentrations de dronédarone par
augmentation de son métabolisme, sans modification notable du
métabolite actif.
+ SIMVASTATINE
Association DECONSEILLEERisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
simvastatine).
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
86
+ VERAPAMIL
Précaution d'emploi
Débuter le traitement par l’antagoniste calcique aux posologies
minimales recommandées, et ajuster les doses en fonction de l’ECG.
Risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez le sujet âgé. Par ailleurs, légère augmentation des
concentrations de dronédarone par diminution de son métabolisme
par l’antagoniste des canaux calciques.
DULOXETINE
Voir aussi : médicaments mixtes adrénergiques-sérotoninergiques - médicaments à l'origine d'un syndrome sérotoninergique
+ CODEINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ ENOXACINE
CONTRE-INDICATIONRisque d’augmentation des effets indésirables de la duloxétine par
diminution de son métabolisme hépatique par l'énoxacine.
+ FLUVOXAMINE
CONTRE-INDICATIONRisque d’augmentation des effets indésirables de la duloxétine par
diminution de son métabolisme hépatique par la fluvoxamine.
+ MEQUITAZINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique et réduction de la posologie du métoprolol pendant
le traitement par la duloxétine et après son arrêt.
Augmentation des concentrations plasmatiques de métoprolol avec
risque de surdosage, par diminution de son métabolisme hépatique
par la duloxétine.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par la duloxétine et après son arrêt.
Augmentation des concentrations plasmatiques de propafénone
avec risque de surdosage, par diminution de son métabolisme
hépatique par la duloxétine.
+ TAMOXIFENE
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par la duloxétine.
+ TETRABENAZINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ TRAMADOL
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
ECONAZOLE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par éconazole et après son
arrêt.
Quelle que soit la voie d'administration de l'éconazole :
augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
ÉDOXABAN
Voir aussi : anticoagulants oraux
+ CICLOSPORINE
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
+ DRONEDARONE
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
87
+ ERYTHROMYCINE
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
+ ITRACONAZOLE
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
EFAVIRENZ
Voir aussi : inducteurs enzymatiques
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique.
+ ATAZANAVIR
Association DECONSEILLEE
Si l’association s’avère nécessaire, adaptation posologique de
l’atazanavir avec surveillance clinique et biologique régulière,
notamment en début d’association.
Risque de baisse de l’efficacité de l’atazanavir par augmentation de
son métabolisme hépatique.
+ ATOVAQUONE
Association DECONSEILLEEDiminution des concentrations plasmatiques d'atovaquone par
l'inducteur enzymatique.
+ DIHYDROERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ ERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ FOSAMPRENAVIR
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'amprénavir.
+ GINKGO
Association DECONSEILLEERisque de moindre efficacité de l'éfavirenz.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
l'inducteur et après son arrêt.
Risque d'hypothyroïdie clinique chez les patients hypothyroïdiens,
par augmentation du métabolisme de la T3 et de la T4.
+ LÉNACAPAVIR
Association DECONSEILLEEDiminution importante des concentrations de lénacapavir.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations d'éfavirenz, avec baisse
d'efficacité.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ RIFABUTINE
Précaution d'emploi
Adaptation éventuelle de la posologie de la rifabutine ou de l'éfavirenz
pendant la durée de l'association.
Diminution importante des concentrations de rifabutine, par
augmentation de son métabolisme hépatique par l’éfavirenz.
Egalement, possibilité de diminution importante des concentrations
d'éfavirenz par la rifabutine.
88
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Diminution des concentrations plasmatiques et de l'efficacité de
l'éfavirenz par augmentation de son métabolisme hépatique par la
rifampicine.
+ VELPATASVIR
Association DECONSEILLEERisque de diminution des concentrations de velpatasvir/sofosbuvir,
avec possible retentissement sur l’efficacité.
+ VORICONAZOLE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite et
adaptation de la posologie du voriconazole et de l'éfavirenz pendant
l'association.
Risque de baisse de l'efficacité du voriconazole par augmentation
de son métabolisme hépatique par l'efavirenz.
ÉLIGLUSTAT
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONChez les patients ayant un génotype de métaboliseurs lents du
CYP2D6, risque de majoration des effets indésirables de l’éliglustat.
ELTROMBOPAG
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
statine.
Risque de majoration de la toxicité des statines, par inhibition de
leur recapture hépatique.
+ OZANIMOD
Association DECONSEILLEERisque d’augmentation des effets indésirables de l’ozanimod.
ELVITÉGRAVIR
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ESTROPROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de
l'elvitégravir.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par l'elvitégravir.
+ ITRACONAZOLE
Précaution d'emploi
Avec l’elvitegravir co-administré avec le cobicistat, surveillance clinique.
Limiter la dose maximale d’itraconazole à 200 mg/j.
Augmentation des concentrations plasmatiques d’elvitegravir par
diminution de son métabolisme par l'itraconazole.
+ KETOCONAZOLE
Précaution d'emploi
Avec l’elvitegravir co-administré avec le cobicistat, surveillance clinique.
Limiter la dose maximale de kétoconazole à 200 mg/j.
Augmentation des concentrations plasmatiques d’elvitegravir par
diminution de son métabolisme par le kétoconazole.
+ RIFABUTINE
A prendre en compteDiminution des concentrations minimales d’elvitégravir.
ENOXACINE
Voir aussi : fluoroquinolones - médicaments abaissant le seuil épileptogène - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et
adsorbants
+ CAFEINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de caféine,
pouvant entraîner excitations et hallucinations, par diminution de
son métabolisme hépatique.
+ DULOXETINE
CONTRE-INDICATIONRisque d’augmentation des effets indésirables de la duloxétine par
diminution de son métabolisme hépatique par l'énoxacine.
+ ROPINIROLE
Précaution d'emploi
Surveillance clinique et réduction de la posologie du ropinirole pendant
le traitement par l'énoxacine et après son arrêt.
Augmentation des concentrations plasmatiques de ropinirole avec
signes de surdosage par diminution de son métabolisme hépatique.
89
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
CONTRE-INDICATIONSurdosage en théophylline par diminution importante de son
métabolisme.
ENTACAPONE
Voir aussi : antiparkinsoniens dopaminergiques - dopaminergiques - inhibiteurs de la catéchol-O-méthyltransférase (COMT) - médicaments à l'origine d'une
hypotension orthostatique
+ FER
Précaution d'emploi
Prendre les sels de fer à distance de l'entacapone (plus de 2 heures si
possible).
Diminution de l'absorption digestive de l'entacapone et du fer par
chélation de celui-ci par l'entacapone.
ENZALUTAMIDE
Voir aussi : inducteurs enzymatiques - inducteurs enzymatiques puissants - médicaments à l'origine d'un hypogonadisme masculin
+ GEMFIBROZIL
Précaution d'emploi
Réduire la dose d’enzalutamide de moitié en cas d’association au
gemfibrozil.
Majoration de la fraction active de l’enzalutamide.
EPLERENONE
Voir aussi : antihypertenseurs sauf alpha-bloquants - diurétiques - diurétiques épargneurs de potassium (seuls ou associés) - hyperkaliémiants - hyponatrémiants -
médicaments abaissant la pression artérielle
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
Précaution d'emploi
Contrôle strict de la kaliémie et de la fonction rénale pendant
l’association.
Majoration du risque d’hyperkaliémie, notamment chez le sujet âgé.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Précaution d'emploi
Contrôle strict de la kaliémie et de la fonction rénale pendant
l’association.
Majoration du risque d’hyperkaliémie, notamment chez le sujet âgé.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques de
l’éplérénone par l'inhibiteur et de ses effets indésirables,
notamment l’hyperkaliémie.
ERGOTAMINE
Voir aussi : alcaloïdes de l'ergot de seigle vasoconstricteurs - substrats à risque du CYP3A4
+ DALFOPRISTINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ DILTIAZEM
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ EFAVIRENZ
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ MACROLIDES (SAUF SPIRAMYCINE)
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (diminution
de l'élimination hépatique de l'ergotamine).
+ OXPRENOLOL
Précaution d'emploi
Surveillance clinique renforcée, en particulier pendant les premières
semaines de l'association.
Ergotisme : quelques cas de spasme artériel avec ischémie des
extrémités ont été observés (addition d'effets vasculaires).
+ PROPRANOLOL
Précaution d'emploi
Surveillance clinique renforcée, en particulier pendant les premières
semaines de l'association.
Ergotisme : quelques cas de spasme artériel avec ischémie des
extrémités ont été observés (addition d'effets vasculaires).
90
+ QUINUPRISTINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ STIRIPENTOL
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition de
l’élimination hépatique de l'alcaloïde de l’ergot de seigle).
+ TRICLABENDAZOLE
CONTRE-INDICATION
Respecter un délai de 24 heures entre l’arrêt du triclabendazole et
l’ergotamine, et inversement.
Ergotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l’alcaloïde de l’ergot de seigle).
ERYTHROMYCINE
Voir aussi : inhibiteurs puissants du CYP3A4 - macrolides (sauf spiramycine) - substances susceptibles de donner des torsades de pointes - torsadogènes (sauf
arsénieux, antiparasitaires, neuroleptiques, méthadone...)
+ AFATINIB
Précaution d'emploi
Il est recommandé d’administrer l'érythromycine le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par l'érythromycine.
+ ALFENTANIL
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par
l'érythromycine.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholesterolémiant.
+ BUSPIRONE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique, avec majoration
importante de la sédation.
+ CARBAMAZEPINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de carbamazépine,
avec signes de surdosage, par inhibition de son métabolisme
hépatique.
+ ÉDOXABAN
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
+ FIDAXOMICINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ GLIBENCLAMIDE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide hypoglycémiant pendant le
traitement par l’érythromycine.
Risque d'hypoglycémie par augmentation de l’absorption et des
concentrations plasmatiques de l’antidiabétique.
+ GLIMEPIRIDE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide hypoglycémiant pendant le
traitement par l’érythromycine.
Risque d'hypoglycémie par augmentation de l’absorption et des
concentrations plasmatiques de l’antidiabétique.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'érythromycine.
91
+ PRAVASTATINE
Précaution d'emploi
Surveillance clinique et biologique pendant le traitement par
l'antibiotique.
Avec l'érythromycine utilisée par voie orale : augmentation de la
concentration plasmatique de la pravastatine par l' érythromycine.
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Association DECONSEILLEESurdosage en théophylline par diminution de son élimination
hépatique, plus particulièrement à risque chez l'enfant.
+ VENLAFAXINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique et ECG ; s'il y a lieu, adaptation de la posologie du
vérapamil pendant le traitement par l'érythromycine et après son arrêt.
Bradycardie et/ou troubles de la conduction auriculo-ventriculaire,
par diminution du métabolisme hépatique du vérapamil par
l'érythromycine.
ESCITALOPRAM
Voir aussi : hyponatrémiants - inhibiteurs sélectifs de la recapture de la sérotonine - médicaments abaissant le seuil épileptogène - médicaments à l'origine d'un
syndrome sérotoninergique - substances susceptibles de donner des torsades de pointes - torsadogènes (sauf arsénieux, antiparasitaires, neuroleptiques,
méthadone...)
+ ESOMEPRAZOLE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ OMEPRAZOLE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
ESMOLOL
Voir aussi : bradycardisants
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ ANTIARYTHMIQUES CLASSE IA
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ DILTIAZEM
ASDEC - PE
Association déconseillée :
- en cas d'altération de la fonction ventriculaire gauche.
Précaution d'emploi :
- si la fonction ventriculaire gauche est normale.
Surveillance clinique et ECG.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
troubles de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ VERAPAMIL
ASDEC - PE
Association déconseillée :
- en cas d'altération de la fonction ventriculaire gauche.
Précaution d'emploi :
- si la fonction ventriculaire gauche est normale.
Surveillance clinique et ECG.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
troubles de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
92
ESOMEPRAZOLE
Voir aussi : antisécrétoires inhibiteurs de la pompe à protons
+ ESCITALOPRAM
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
ESTRAMUSTINE
Voir aussi : cytotoxiques - médicaments, bradykinine et angio-œdème
+ ACIDE CLODRONIQUE
Précaution d'emploi
Surveillance clinique au cours de l’association.
Risque d’augmentation des concentrations plasmatiques
d’estramustine par le clodronate.
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium à distance de l'estramustine (plus de 2
heures, si possible).
Diminution de l'absorption digestive de l'estramustine.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Association DECONSEILLEERisque de majoration des effets indésirables à type d'oedème
angio-neurotique (angio-oedème).
ESTROGÈNES NON CONTRACEPTIFS
(diethylstilbestrol, estétrol, estradiol, estriol, estrogènes conjugués, estrone, promestriene)
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique ; adaptation éventuelle des doses de
l'hormone thyroïdienne chez les femmes ménopausées prenant des
estrogènes.
Risque d'hypothyroïdie clinique en cas d'estrogénothérapie
substitutive.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant l'administration de l'inducteur et après son
arrêt.
Diminution de l'efficacité de l'estrogène.
+ OXCARBAZEPINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant le traitement par l'oxcarbazépine et après
son arrêt.
Risque de diminution de l'efficacité du traitement hormonal, par
augmentation de son métabolisme hépatique par l'oxcarbazépine.
ESTROPROGESTATIFS CONTRACEPTIFS
(estradiol, ethinylestradiol)
+ APREPITANT
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de
l’aprépitant.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par l'aprépitant.
+ BOSENTAN
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du bosentan.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par le bosentan.
+ ELVITÉGRAVIR
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de
l'elvitégravir.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par l'elvitégravir.
+ FELBAMATE
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du
felbamate.
Risque de diminution de l’efficacité contraceptive, pendant le
traitement et un cycle après l’arrêt du traitement par le felbamate,
en raison de son potentiel inducteur enzymatique.
+ GRISEOFULVINE
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de de la
griséofulvine.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par la
griséofulvine.
93
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEE
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de
l’inducteur.
Diminution de l'efficacité contraceptive, par augmentation du
métabolisme hépatique du contraceptif hormonal par l'inducteur.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Association DECONSEILLEE
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du ritonavir.
Risque de diminution de l'efficacité contraceptive par diminution
des concentrations en contraceptif hormonal, dûe à l'augmentation
de son métabolisme hépatique par le ritonavir.
+ LAMOTRIGINE
ASDEC - PE
Association déconseillée:
- Eviter de mettre en route une contraception orale pendant la période
d'ajustement posologique de la lamotrigine.
Précaution d'emploi:
- Surveillance clinique et adaptation de la posologie de la lamotrigine
lors de la mise en route d'une contraception orale et après son arrêt.
Diminution des concentrations et de l’efficacité de la lamotrigine par
augmentation de son métabolisme hépatique.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques du contraceptif
hormonal, en raison de l'effet inducteur enzymatique du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet dont les conséquences peuvent être éventuellement graves
(survenue d'une grossesse).
+ MODAFINIL
Association DECONSEILLEE
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du modafinil.
Risque de diminution de l’efficacité contraceptive, pendant le
traitement et un cycle après l’arrêt du traitement par le modafinil, en
raison de son potentiel inducteur enzymatique.
+ RUFINAMIDE
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du
rufinamide.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par le rufinamide.
+ TOPIRAMATE
Association DECONSEILLEE
Si l’association s’avère nécessaire, utiliser une méthode additionnel de
type mécanique pendant la durée de l’association et un cycle suivant
l’arrêt du topiramate.
Pour des doses de topiramate >= 200 mg/jour :
Risque de diminution de l’efficacité contraceptive par diminution
des concentrations en estrogène.
+ VÉMURAFÉNIB
Association DECONSEILLEERisque de diminution des concentrations des estroprogestatifs,
avec pour conséquence un risque d’inefficacité.
ESZOPICLONE
Voir aussi : benzodiazépines et apparentés - hypnotiques - médicaments sédatifs
+ INHIBITEURS PUISSANTS DU CYP3A4
CI - PE
Contre-indication
- chez les patients âgés
Précaution d'emploi
En cas d’association chez les sujets non âgés, une réduction de la dose
d’eszopiclone peut être nécessaire.
Augmentation de l'effet sédatif de l’eszopiclone.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique. Utiliser éventuellement un autre hypnotique.
Risque de diminution des concentrations plasmatiques et de
l'efficacité de l’eszopiclone par augmentation de son métabolisme
hépatique par la rifampicine.
ETANERCEPT
Voir aussi : anti-TNF alpha
+ ANAKINRA
Association DECONSEILLEERisque accru d'infections graves et de neutropénies.
ÉTELCALCÉTIDE
+ CINACALCET
Association DECONSEILLEERisque d’hypocalcémie sévère.
94
ETHINYLESTRADIOL
Voir aussi : estroprogestatifs contraceptifs
+ DASABUVIR
CONTRE-INDICATIONAugmentation de l’hépatotoxicité.
+ GLÉCAPRÉVIR + PIBRENTASVIR
CONTRE-INDICATIONAugmentation de l’hépatotoxicité avec la bithérapie.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation de l’hépatotoxicité.
ETHOSUXIMIDE
Voir aussi : anticonvulsivants métabolisés
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, dosage plasmatique de l'éthosuximide et
augmentation éventuelle de sa posologie.
Diminution des concentrations plasmatiques d'éthosuximide.
ETOPOSIDE
Voir aussi : cytotoxiques
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEE
Si l'association s'avère nécessaire, surveillance clinique et adaptation
éventuelle de la posologie d’étoposide pendant l’association, et 1 à 2
semaines après l’arrêt de l’inducteur.
Diminution des concentrations plasmatiques d’étoposide par
l’inducteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques d’étoposide
par le millepertuis.
ETRAVIRINE
+ ATAZANAVIR
Association DECONSEILLEERisque de diminution des concentrations plasmatiques d’atazanavir
par l’étravirine.
+ CLARITHROMYCINE
A prendre en compteDans le traitement des infections à Mycobacterium avium complex,
risque de diminution de l’efficacité de la clarithromycine par
augmentation de son métabolisme hépatique par l’étravirine.
+ COBICISTAT
Association DECONSEILLEERisque de diminution des concentrations plasmatiques du
cobicistat par l’étravirine.
+ DARUNAVIR
Association DECONSEILLEERisque de diminution des concentrations plasmatiques du
darunavir par l’étravirine.
+ GRAZOPREVIR + ELBASVIR
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
grazoprevir/elbasvir par l’étravirine.
EVEROLIMUS
Voir aussi : immunosuppresseurs - substrats à risque du CYP3A4
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines d’évérolimus, éventuellement
adaptation de la posologie et contrôle de la fonction rénale, pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines de l’évérolimus par la
ciclosporine. La néphrotoxicité de la ciclosporine est également
augmentée lors de l’association.
95
+ OMBITASVIR + PARITAPRÉVIR
Association DECONSEILLEE
Si l’association s’avère nécessaire, contrôle strict de la fonction rénale,
dosage des concentrations sanguines de l'immunosuppresseur et
adaptation éventuelle de la posologie.
En association avec le ritonavir : augmentation significative des
concentrations de l’immunosuppresseur avec risque de majoration
de sa toxicité par la bithérapie.
+ VERAPAMIL
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines de l'évérolimus par
diminution de son métabolisme hépatique par le vérapamil.
EXEMESTANE
+ RIFAMPICINE
A prendre en compteRisque de diminution de l'efficacité de l'exemestane par
augmentation de son métabolisme hépatique par l'inducteur
enzymatique.
EZETIMIBE
Voir aussi : médicaments à l'origine d'atteintes musculaires
+ CICLOSPORINE
Association DECONSEILLEED’une part, risque majoré d'effets indésirables (concentration-
dépendants) à type de rhabdomyolyse, par augmentation des
concentrations d’ézétimibe ; d’autre part, possible augmentation
des concentrations de ciclosporine.
+ FENOFIBRATE
Association DECONSEILLEERisque de lithiase biliaire par augmentation de l’excrétion biliaire du
cholestérol.
FELBAMATE
Voir aussi : anticonvulsivants métabolisés
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation éventuelle
des posologies des deux anticonvulsivants.
Augmentation des concentrations plasmatiques du métabolite actif
de la carbamazépine. De plus, diminution des concentrations
plasmatiques de felbamate par augmentation de son métabolisme
hépatique par la carbamazépine.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du
felbamate.
Risque de diminution de l’efficacité contraceptive, pendant le
traitement et un cycle après l’arrêt du traitement par le felbamate,
en raison de son potentiel inducteur enzymatique.
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénobarbital avec adaptation de la posologie si besoin.
Diminution des concentrations plasmatiques et de l'efficacité du
felbamate et augmentation des concentrations plasmatiques du
phénobarbital, avec risque de surdosage.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
phénytoïne et si besoin, adaptation de sa posologie pendant le
traitement par le felbamate.
Augmentation des concentrations plasmatiques de phénytoïne
avec risque de surdosage, par inhibition de son métabolisme par le
felbamate.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique, contrôle biologique et adaptation éventuelle de la
posologie du valproate ou du valpromide pendant le traitement par le
felbamate et après son arrêt.
Augmentation des concentrations plasmatiques de l'acide
valproïque, avec risque de surdosage.
FENOFIBRATE
Voir aussi : fibrates - médicaments à l'origine d'atteintes musculaires
+ CICLOSPORINE
Précaution d'emploi
Surveillance clinique et biologique de la fonction rénale, pendant et
après l'association.
Risque d'augmentation de la néphrotoxicité de la ciclosporine.
+ EZETIMIBE
Association DECONSEILLEERisque de lithiase biliaire par augmentation de l’excrétion biliaire du
cholestérol.
96
FENTANYL
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier III - morphiniques - médicaments sédatifs
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEE
Préférer un autre morphinique.
Diminution des concentrations plasmatiques de fentanyl par
augmentation de son métabolisme hépatique par l'inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
l’analgésique opiacé en cas de traitement par un inhibiteur puissant du
CYP3A4.
Risque d'augmentation de l’effet dépresseur respiratoire de
l’analgésique opiacé par légère diminution de son métabolisme
hépatique.
+ RIFAMPICINE
Association DECONSEILLEE
Préférer un autre morphinique.
Diminution des concentrations plasmatiques de fentanyl par
augmentation de son métabolisme hépatique par la rifampicine.
FER
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ SELS DE FER PAR VOIE INJECTABLE
Association DECONSEILLEELipothymie, voire choc attribué à la libération rapide du fer de sa
forme complexe et à la saturation de la sidérophiline.
+ ACIDE ACETOHYDROXAMIQUE
A prendre en compteDiminution de l'absorption digestive de ces deux médicaments par
chélation du fer.
+ BICTÉGRAVIR
Précaution d'emploi
Prendre le bictégravir au moins 2 heures avant les sels de fer, ou en
même temps qu’un repas.
Diminution de près des deux tiers de l'absorption du bictégravir en
cas d’ingestion simultanée ou à jeun.
+ BISPHOSPHONATES
Précaution d'emploi
Prendre les sels de fer à distance des bisphosphonates (de 30 minutes
au minimum à plus de 2 heures, si possible, selon le bisphosphonate).
Pour les sels de fer administrés par voie orale : diminution de
l'absorption digestive des bisphosphonates.
+ CALCIUM
Précaution d'emploi
Prendre les sels de fer à distance des repas et en l'absence de calcium.
Avec les sels de fer par voie orale : diminution de l'absorption
digestive des sels de fer.
+ CYCLINES
Précaution d'emploi
Prendre les sels de fer à distance des cyclines (plus de 2 heures, si
possible).
Diminution de l'absorption digestive des cyclines et du fer
+ ENTACAPONE
Précaution d'emploi
Prendre les sels de fer à distance de l'entacapone (plus de 2 heures si
possible).
Diminution de l'absorption digestive de l'entacapone et du fer par
chélation de celui-ci par l'entacapone.
+ FLUOROQUINOLONES
Précaution d'emploi
Prendre les sels de fer à distance des fluoroquinolones (plus de 2
heures, si possible).
Diminution de l'absorption digestive des fluoroquinolones.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Prendre les hormones thyroïdiennes à distance du fer (plus de 2
heures, si possible).
Diminution de l'absorption digestive des hormones thyroïdiennes.
+ INHIBITEURS D'INTÉGRASE
Précaution d'emploi
Prendre les sels de fer à distance de l’antirétroviral (plus de 2 heures, si
possible).
Diminution de l'absorption digestive des inhibiteurs d’intégrase.
97
+ LEVODOPA
Précaution d'emploi
Prendre les sels de fer à distance de la lévodopa (plus de 2 heures si
possible).
Diminution de l'absorption digestive de la lévodopa.
+ METHYLDOPA
Précaution d'emploi
Prendre les sels de fer à distance de la méthyldopa (plus de deux
heures, si possible).
Diminution de l'absorption digestive de la méthyldopa (formation de
complexes).
+ PENICILLAMINE
Précaution d'emploi
Prendre les sels de fer à distance de la pénicillamine (plus de 2 heures,
si possible).
Diminution de l'absorption digestive de la pénicillamine.
+ ROXADUSTAT
Précaution d'emploi
Prendre le roxadustat à distance des sels de fer (plus de 1 heure, si
possible).
La prise de cation divalent peut diminuer l’absorption intestinale et,
potentiellement, l’efficacité du roxadustat pris simultanément.
+ STRONTIUM
Précaution d'emploi
Prendre le strontium à distance des sels de fer (plus de deux heures, si
possible).
Diminution de l'absorption digestive du strontium.
+ TRIENTINE
Précaution d'emploi
Prendre la trientine à distance des sels de fer.
Diminution des concentrations de fer sérique.
+ ZINC
Précaution d'emploi
Prendre les sels de fer à distance du zinc (plus de 2 heures si possible).
Diminution de l’absorption digestive du zinc par le fer.
FEXOFENADINE
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la féxofénadine par
le millepertuis.
FIBRATES
(bezafibrate, ciprofibrate, fenofibrate, gemfibrozil)
+ FIBRATES (AUTRES)
CONTRE-INDICATIONRisque majoré d'effets indésirables à type de rhabdomyolyse et
d'antagonisme pharmacodynamique entre les deux molécules.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par le fibrate et 8 jours après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ COLCHICINE
Précaution d'emploi
Surveillance clinique et biologique, particulièrement au début de
l’association.
Risque de majoration des effets indésirables musculaires de ces
substances, et notamment de rhabdomyolyse.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
CI - ASDEC
L'association d'un fibrate et d'une statine est au minmum déconseillée.
Avec la simvastatine, ne pas dépasser 10 mg ( cette restriction de
doses ne concerne pas le fénofibrate).
La contre-indication s'applique :
- entre le gemfibrozil et la simvastatine
- pour des doses de rosuvastatine de 40 mg
Risque d'addition d'effets indésirables (dose-dépendants) à type de
rhabdomyolyse. En outre, avec le gemfibrozil, diminution du
métabolisme de la simvastatine et de la rosuvastatine, ce qui
majore le risque musculaire, ainsi que la néphrotoxicité de la
rosuvastatine.
98
FIDAXOMICINE
+ AMIODARONE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ CICLOSPORINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ CLARITHROMYCINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ DRONEDARONE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ ERYTHROMYCINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ KETOCONAZOLE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ VERAPAMIL
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
FINGOLIMOD
Voir aussi : bradycardisants
+ BRADYCARDISANTS
Association DECONSEILLEE
Surveillance clinique et ECG continu pendant les 6 heures suivant la
première dose voire 2 heures de plus, jusqu'au lendemain si nécessaire.
Potentialisation des effets bradycardisants pouvant avoir des
conséquences fatales. Les bêta-bloquants sont d’autant plus à
risque qu’ils empêchent les mécanismes de compensation
adrénergique.
FLUCLOXACILLINE
Voir aussi : pénicillines
+ PARACETAMOL
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance étroite avec mesure de
la 5-oxoproline urinaire.
Risque accru d'acidose métabolique à trou anionique élevé,
notamment en cas d'insuffisance rénale sévère, de sepsis, de
facteurs prédisposant à la déplétion en glutathion (malnutrition,
alcoolisme chronique…), ainsi qu’en cas d’utilisation de
paracétamol aux doses quotidiennes maximales.
+ VORICONAZOLE
Association DECONSEILLEEDiminution des concentrations de voriconazole, avec risque
d'inefficacité de l'antifongique azolé.
FLUCONAZOLE
+ ABROCITINIB
Précaution d'emploi
Réduire la posologie de l’abrocitinib de moitié en cas de traitement par
le fluconazole.
Risque de majoration des effets indésirables de l’abrocitinib par
diminution de son métabolisme.
+ ALFENTANIL
Précaution d'emploi
Adapter la posologie de l'alfentanil en cas de traitement par le
fluconazole.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
+ AMIODARONE
Précaution d'emploi
Surveillance clinique, particulièrement aux fortes doses de fluconazole
(800 mg/j).
Risque d’allongement de l’intervalle QT.
99
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par le fluconazole et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ APIXABAN
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l'apixaban par le
fluconazole, avec majoration du risque de saignement.
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles de l'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables concentration-dépendants à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
statine).
+ CARBAMAZEPINE
Précaution d'emploi
Adapter la posologie de carbamazépine, pendant et après l’arrêt du
traitement antifongique.
Pour des doses de fluconazole >= 200 mg par jour : augmentation
possible des effets indésirables de la carbamazépine.
+ COLCHICINE
Association DECONSEILLEEAugmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
+ DOMPERIDONE
CONTRE-INDICATIONRisque de troubles du rythme ventriculaire, notamment de torsades
de pointes.
+ HALOFANTRINE
Association DECONSEILLEE
Si cela est possible, interrompre le fluconazole. Si l'association ne peut
être évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le fluconazole.
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de sa posologie pendant
l'association et après son arrêt.
Risque d'augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme et de la
créatininémie.
+ IVACAFTOR (SEUL OU ASSOCIÉ)
Précaution d'emploi
Se référer à l'AMM pour les adaptations posologiques.
Augmentation des concentrations d’ivacaftor, avec risque de
majoration des effets indésirables.
+ LOSARTAN
A prendre en compteRisque de diminution de l’efficacité du losartan, par inhibition de la
formation de son métabolite actif par le fluconazole.
+ MIDAZOLAM
Précaution d'emploi
Surveillance clinique et réduction de la posologie de midazolam en cas
de traitement par le fluconazole.
Augmentation des concentrations plasmatiques de midazolam par
diminution de son métabolisme hépatique, avec majoration de la
sédation.
+ NEVIRAPINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
névirapine.
Doublement des concentrations de névirapine avec risque
d'augmentation de ses effets indésirables.
+ OLAPARIB
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par le
fluconazole.
100
+ OXYCODONE
Association DECONSEILLEEMajoration des effets indésirables, notamment respiratoires, de
l’oxycodone par diminution de son métabolisme hépatique par le
fluconazole.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et biologique étroite.
Augmentation des concentrations plasmatiques de phénytoïne
pouvant atteindre des valeurs toxiques. Mécanisme invoqué :
inhibition du métabolisme hépatique de la phénytoïne.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ RIFABUTINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'accroissement des effets indésirables de la rifabutine
(uvéites), par augmentation de ses concentrations et de celles de
son métabolite actif.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l'efficacité du
fluconazole par augmentation de son métabolisme par la
rifampicine.
+ RIVAROXABAN
Association DECONSEILLEEAugmentation des concentrations plasmatiques du rivaroxaban par
le fluconazole, avec majoration du risque de saignement.
+ SIMVASTATINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d’interaction.
Risque majoré d'effets indésirables concentration-dépendants à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
simvastatine).
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide pendant le traitement par le
fluconazole.
Augmentation du temps de demi-vie du sulfamide avec survenue
possible de manifestations d'hypoglycémie.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par le fluconazole et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution de la clairance de la théophylline).
+ TOLVAPTAN
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
+ VINCA-ALCALOÏDES CYTOTOXIQUES
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque de majoration de la toxicité de l’antimitotique par diminution
de son métabolisme hépatique par le fluconazole.
FLUCYTOSINE
+ CYTOTOXIQUES
A prendre en compteRisque de majoration de la toxicité hématologique
+ GANCICLOVIR
A prendre en compteRisque de majoration de la toxicité hématologique.
+ IMMUNOSUPPRESSEURS
A prendre en compteRisque de majoration de la toxicité hématologique.
101
+ VALGANCICLOVIR
A prendre en compteRisque de majoration de la toxicité hématologique.
+ ZIDOVUDINE
Précaution d'emploi
Contrôle plus fréquent de l'hémogramme.
Augmentation de la toxicité hématologique (addition d'effets de
toxicité médullaire).
FLUDARABINE
Voir aussi : cytotoxiques
+ PENTOSTATINE
Association DECONSEILLEEMajoration du risque de toxicité pulmonaire pouvant être fatale.
FLUOROQUINOLONES
(ciprofloxacine, délafloxacine, enoxacine, levofloxacine, lomefloxacine, moxifloxacine, norfloxacine, ofloxacine, pefloxacine)
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la fluoroquinolone et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ FER
Précaution d'emploi
Prendre les sels de fer à distance des fluoroquinolones (plus de 2
heures, si possible).
Diminution de l'absorption digestive des fluoroquinolones.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
A prendre en comptePossible majoration du risque de tendinopathie, voire de rupture
tendineuse (exceptionnelle), particulièrement chez les patients
recevant une corticothérapie prolongée.
+ MYCOPHENOLATE MOFETIL
A prendre en compteDiminution des concentrations de l’acide mycophénolique d’environ
un tiers, avec risque potentiel de baisse d’efficacité.
+ STRONTIUM
Précaution d'emploi
Prendre le strontium à distance des fluoroquinolones (plus de deux
heures, si possible).
Diminution de l'absorption digestive du strontium.
+ SUCRALFATE
Précaution d'emploi
Prendre le sucralfate à distance des fluoroquinolones (plus de 2 heures,
si possible).
Diminution de l'absorption digestive des fluoroquinolones.
+ ZINC
Précaution d'emploi
Prendre les sels de zinc à distance des fluoroquinolones (plus de 2
heures, si possible).
Diminution de l'absorption digestive des fluoroquinolones.
FLUOROURACILE (ET, PAR EXTRAPOLATION, AUTRES FLUOROPYRIMIDINES)
(capecitabine, fluorouracile, giméracil, otéracil, tegafur)
+ ACIDE FOLINIQUE
A prendre en comptePotentialisation des effets, à la fois cytostatiques et indésirables, du
fluoro-uracile.
+ ANTIVITAMINES K
Association DECONSEILLEE
Si elle ne peut être évitée, contrôle plus fréquent de l'INR. Adaptation de
la posologie de l'antivitamine K pendant le traitement par le cytotoxique
et 8 jours après son arrêt.
Augmentation importante de l'effet de l'antivitamine K et du risque
hémorragique.
+ INTERFERON ALFA
A prendre en compteAugmentation de la toxicité gastro-intestinale du fluorouracile.
102
+ METRONIDAZOLE
A prendre en compteAugmentation de la toxicité du fluoro-uracile par diminution de sa
clairance.
+ ORNIDAZOLE
A prendre en compteAugmentation de la toxicité du fluoro-uracile par diminution de sa
clairance.
FLUOXETINE
Voir aussi : hyponatrémiants - inhibiteurs sélectifs de la recapture de la sérotonine - médicaments abaissant le seuil épileptogène - médicaments à l'origine d'un
syndrome sérotoninergique
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
carbamazépine et réduction éventuelle de la posologie de la
carbamazépine pendant le traitement par l'antidépresseur
sérotoninergique et après son arrêt.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
+ CODEINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ MEQUITAZINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
métoprolol pendant la durée du traitement par la fluoxétine et après son
arrêt.
Risque de majoration des effets indésirables du métoprolol, avec
notamment bradycardie excessive, par inhibition de son
métabolisme par la fluoxétine.
+ NEBIVOLOL
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
nébivolol pendant la durée du traitement par l’antidépresseur et après
son arrêt.
Risque de majoration des effets indésirables du nébivolol avec
notamment bradycardie excessive, par inhibition de son
métabolisme par l’antidépresseur.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et éventuellement contrôle des concentrations
plasmatiques de phénytoïne. Si besoin, adaptation posologique pendant
le traitement par la fluoxétine et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage, par inhibition du métabolisme de la
phénytoïne.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ RISPERIDONE
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique de la
rispéridone.
Augmentation de la fraction active de la rispéridone par diminution
de son métabolisme hépatique par la fluoxétine, avec risque de
majoration des effets indésirables.
+ TAMOXIFENE
Association DECONSEILLEEBaisse de l’efficacité du tamoxifène, par inhibition de la formation
de son métabolite actif par la fluoxétine.
+ TETRABENAZINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ TRAMADOL
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
103
FLUVASTATINE
Voir aussi : inhibiteurs de l'HMG-CoA réductase (statines) - médicaments à l'origine d'atteintes musculaires
+ CICLOSPORINE
Précaution d'emploi
Surveillance clinique et biologique pendant l’association.
Augmentation modérée des concentrations de fluvastatine, avec
risque musculaire non exclu.
FLUVOXAMINE
Voir aussi : hyponatrémiants - inhibiteurs sélectifs de la recapture de la sérotonine - médicaments abaissant le seuil épileptogène - médicaments à l'origine d'un
syndrome sérotoninergique
+ ABROCITINIB
Précaution d'emploi
Réduire la posologie de l’abrocitinib de moitié en cas de traitement par
la fluvoxamine.
Risque de majoration des effets indésirables de l’abrocitinib par
diminution de son métabolisme.
+ AGOMELATINE
CONTRE-INDICATIONAugmentation des concentrations d'agomélatine, avec risque de
majoration des effets indésirables.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
carbamazépine et réduction éventuelle de la posologie de la
carbamazépine pendant le traitement par l'antidépresseur
sérotoninergique et après son arrêt.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
+ CLOZAPINE
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie de la
clozapine pendant le traitement par la fluvoxamine et après son arrêt.
Augmentation des concentrations plasmatiques de clozapine avec
signes de surdosage.
+ DULOXETINE
CONTRE-INDICATIONRisque d’augmentation des effets indésirables de la duloxétine par
diminution de son métabolisme hépatique par la fluvoxamine.
+ LIDOCAINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations plasmatiques de la lidocaïne pendant et après l’arrêt de
l’association. Adaptation, si besoin, de la posologie de la lidocaïne.
Augmentation des concentrations plasmatiques de la lidocaïne
avec possibilités d’effets indésirables neurologiques et cardiaques
(diminution de la clairance hépatique de la lidocaïne).
+ METHADONE
Précaution d'emploi
Surveillance clinique et électrocardiographique renforcée ; si besoin,
adaptation de la posologie de la méthadone pendant le traitement par la
fluvoxamine et après son arrêt.
Augmentation des concentrations plasmatiques de méthadone
avec surdosage et risque majoré d’allongement de l’intervalle QT et
de troubles du rythme ventriculaire, notamment de torsades de
pointes.
+ MEXILETINE
Précaution d'emploi
Surveillance clinique et ECG. Adaptation de la posologie de la
méxilétine pendant le traitement par la fluvoxamine et après son arrêt.
Risque de majoration des effets indésirables de la méxilétine, par
inhibition de son métabolisme par la fluvoxamine.
+ OLANZAPINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de
l’olanzapine pendant le traitement par fluvoxamine.
Augmentation des concentrations de l’olanzapine, avec risque de
majoration des effets indésirables, par diminution de son
métabolisme hépatique par la fluvoxamine.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et éventuellement contröle des concentrations
plamatiques de phénytoïne. Si besoin, adaptation posologique de la
phénytoïne pendant le traitement par la fluvoxamine et après son arrët.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage, par inhibition du métabolisme hépatique
de la phénytoïne.
+ PIRFENIDONE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de pirfenidone
avec signes de surdosage.
+ PROPRANOLOL
Précaution d'emploi
Surveillance clinique accrue et, si besoin, adaptation de la posologie du
propranolol pendant le traitement par la fluvoxamine et après son arrêt.
Augmentation des concentrations plasmatiques de propranolol par
inhibition de son métabolisme hépatique, avec majoration de
l'activité et des effets indésirables, par exemple : bradycardie
importante.
104
+ ROPINIROLE
Précaution d'emploi
Surveillance clinique et réduction de la posologie du ropinirole pendant
le traitement par fluvoxamine et après son arrêt.
Augmentation des concentrations de ropinirole, avec risque de
surdosage, par diminution de son métabolisme hépatique par la
fluvoxamine.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; si
besoin, adaptation de la posologie de la théophylline pendant le
traitement par la fluvoxamine et après son arrêt.
Augmentation de la théophyllinémie avec signes de surdosage
(diminution du métabolisme hépatique de la théophylline).
FOLATES
(acide folinique, acide folique)
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques, et
adaptation, s'il y a lieu, de la posologie du phénobarbital pendant la
supplémentation folique et après son arrêt.
Diminution des concentrations plasmatiques du phénobarbital, par
augmentation de son métabolisme dont les folates représentent un
des cofacteurs.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne. Adaptation éventuelle de la posologie de la phénytoïne
pendant la supplémentation folique et après son arrêt.
Diminution des concentrations plasmatiques de phénytoïne par
augmentation de son métabolisme dont les folates représentent un
des cofacteurs.
FOSAMPRENAVIR
Voir aussi : inhibiteurs de protéases boostés par ritonavir
+ EFAVIRENZ
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'amprénavir.
+ MARAVIROC
Association DECONSEILLEEDiminution significative des concentrations d’amprénavir pouvant
conduire à une perte de la réponse virologique.
+ NEVIRAPINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'amprénavir.
FOSCARNET
Voir aussi : médicaments néphrotoxiques
+ PENTAMIDINE
Précaution d'emploi
Surveillance de la calcémie et supplémentation si nécessaire.
Risque d'hypocalcémie sévère.
FOSTAMATINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés
+ ROSUVASTATINE
Précaution d'emploi
Surveillance clinique et biologique, avec adaptation de la posologie de
rosuvastatine si nécessaire.
Doublement moyen des concentrations plasmatiques de la
rosuvastatine.
FOSTEMSAVIR
+ INDUCTEURS ENZYMATIQUES
CI - APEC
Contre-indication :
- avec la rifampicine, la carbamazépine, la phénytoïne, l’enzalutamide
A prendre en compte :
- avec les autres inducteurs
Diminution significative des concentrations de fotemsavir avec la
rifampicine, avec risque de réduction de la réponse virologique.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution significative des concentrations de
fostemsavir avec le millepertuis, avec réduction de la réponse
virologique.
105
+ MITOTANE
CONTRE-INDICATIONDiminution significative des concentrations de fostemsavir avec la
rifampicine, avec risque de réduction de la réponse virologique.
Éventualité non exclue avec le mitotane.
+ ROSUVASTATINE
Précaution d'emploi
Débuter par la dose minimale de rosuvastatine. Surveillance clinique
régulière.
Augmentation modérée des concentrations de rosuvastatine.
FOTEMUSTINE
Voir aussi : cytotoxiques
+ DACARBAZINE
Précaution d'emploi
Ne pas utiliser simultanément mais respecter un délai d'une semaine
entre la dernière administration de fotémustine et le premier jour de la
cure de dacarbazine.
Avec la dacarbazine à doses élevées : risque de toxicité
pulmonaire (syndrome de détresse respiratoire aiguë de l'adulte).
FUROSEMIDE
Voir aussi : antihypertenseurs sauf alpha-bloquants - diurétiques - diurétiques de l'anse - diurétiques hypokaliémiants - hypokaliémiants - hyponatrémiants -
médicaments abaissant la pression artérielle - médicaments ototoxiques
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Utiliser éventuellement des doses plus élevées de furosémide.
Diminution de l'effet diurétique pouvant atteindre 50 %.
GANCICLOVIR
Voir aussi : médicaments néphrotoxiques
+ DIDANOSINE
Association DECONSEILLEERisque d'augmentation des effets indésirables de la didanosine, et
notamment la toxicité mitochondriale, par augmentation importante
de ses concentrations. De plus risque de diminution de l'efficacité
du ganciclovir par diminution de ses concentrations, si les deux
médicaments sont ingérés à moins de 2 heures d'intervalle.
+ FLUCYTOSINE
A prendre en compteRisque de majoration de la toxicité hématologique.
+ MARIBAVIR
CONTRE-INDICATIONAntagonisme de la phosporylation et donc de l'effet
pharmacologique du ganciclovir par le maribavir.
+ ZIDOVUDINE
Précaution d'emploi
Arrêter de façon transitoire la zidovudine ; contrôler la NFS et
réintroduire, si possible, la zidovudine à doses faibles.
Augmentation de la toxicité hématologique (addition d'effets de
toxicité médullaire).
GEMFIBROZIL
Voir aussi : fibrates - médicaments à l'origine d'atteintes musculaires
+ DASABUVIR
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques du
dasabuvir par le gemfibrozil.
+ ENZALUTAMIDE
Précaution d'emploi
Réduire la dose d’enzalutamide de moitié en cas d’association au
gemfibrozil.
Majoration de la fraction active de l’enzalutamide.
+ OZANIMOD
A prendre en compteAugmentation des concentrations des métabolites actifs de
l’onazimod.
+ PACLITAXEL
Précaution d'emploi
Surveillance clinique et biologique étroite et adaptation de la posologie
du paclitaxel pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
paclitaxel par inhibition de son métabolisme hépatique par le
gemfibrozil.
106
+ REPAGLINIDE
CONTRE-INDICATIONRisque d'hypoglycémie sévère voire de coma, par augmentation
importante des concentrations plasmatiques de repaglinide par le
gemfibrozil.
+ ROXADUSTAT
Précaution d'emploi
Surveillance clinique et biologique (hémoglobine).
Augmentation de l’exposition du roxadustat, par diminution de son
métabolisme par le gemfibrozil.
+ SELEXIPAG
CONTRE-INDICATIONRisque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
+ TUCATINIB
Association DECONSEILLEEAugmentation importante des concentrations de tucatinib par
diminution de son métabolisme par le gemfibrozil.
GILTÉRITINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de gilteritinib avec
risque de perte d’efficacité.
GINKGO
+ EFAVIRENZ
Association DECONSEILLEERisque de moindre efficacité de l'éfavirenz.
GIVOSIRAN
+ THEOPHYLLINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Risque d’augmentation de la théophyllinémie avec signes de
surdosage par diminution de son métabolisme hépatique.
GLASDÉGIB
+ INDUCTEURS ENZYMATIQUES
ASDEC - PE
Association déconseillée
- avec la rifampicine
- avec les anticonvulsivants inducteurs enzymatiques (carbamazépine,
phénytoïne, phénobarbital…)
Précaution d'emploi
- avec les autres inducteurs
- si l’association ne peut être évitée, augmenter la dose de glasdégib.
Diminution, éventuellement importante selon l'inducteur, des
concentrations de glasdégib par augmentation de son
métabolisme, avec risque d'inefficacité.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Risque de majoration des effets indésirables du glasdégib par
diminution de son métabolisme.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
GLÉCAPRÉVIR + PIBRENTASVIR
(Glécaprévir, pibrentasvir)
+ ATAZANAVIR
CONTRE-INDICATIONAugmentation de l’hépatotoxicité avec la bithérapie.
+ ATORVASTATINE
CONTRE-INDICATIONAugmentation importante des concentrations plasmatiques
d’atorvastatine par la bithérapie, avec risque majoré d’effets
indésirables (concentration-dépendants) à type de rhabdomyolyses.
107
+ DABIGATRAN
CONTRE-INDICATIONDoublement des concentrations plasmatiques de dabigatran, avec
majoration du risque de saignements.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par glécaprévir/ pibrentasvir.
Augmentation des concentrations plasmatiques de la digoxine par
la bithérapie.
+ ETHINYLESTRADIOL
CONTRE-INDICATIONAugmentation de l’hépatotoxicité avec la bithérapie.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la bithérapie par
augmentation de son métabolisme par le millepertuis.
+ SIMVASTATINE
CONTRE-INDICATIONAugmentation importante des concentrations plasmatiques de
simvastatine par la bithérapie, avec risque majoré d’effets
indésirables (concentration-dépendants) à type de rhabdomyolyses .
GLIBENCLAMIDE
Voir aussi : antabuse (réaction) - sulfamides hypoglycémiants
+ BOSENTAN
Précaution d'emploi
Surveillance de la glycémie, adaptation du traitement si besoin, et
surveillance des constantes biologiques hépatiques.
Risque de moindre efficacité du glibenclamide par diminution de
ses concentrations plasmatiques, en raison de l'effet inducteur du
bosentan. Par ailleurs, des cas d'hépatotoxicité ont été rapportés
lors de l'association.
+ ERYTHROMYCINE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide hypoglycémiant pendant le
traitement par l’érythromycine.
Risque d'hypoglycémie par augmentation de l’absorption et des
concentrations plasmatiques de l’antidiabétique.
GLIMEPIRIDE
Voir aussi : sulfamides hypoglycémiants
+ ERYTHROMYCINE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide hypoglycémiant pendant le
traitement par l’érythromycine.
Risque d'hypoglycémie par augmentation de l’absorption et des
concentrations plasmatiques de l’antidiabétique.
GLINIDES
(nateglinide, repaglinide)
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêta-bloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
GLIPIZIDE
Voir aussi : antabuse (réaction) - sulfamides hypoglycémiants
+ VORICONAZOLE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide pendant et après le traitement
par voriconazole.
Risque d’augmentation des concentrations plasmatiques du
glipizide à l’origine d’hypoglycémies potentiellement sévères.
GLIPTINES
(linagliptine, saxagliptine, sitagliptine, vildagliptine)
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
108
+ INHIBITEURS DE L'ENZYME DE CONVERSION
A prendre en compteRisque de majoration de la survenue d'un angio-œdème d'origine
bradykinique pouvant être fatal.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Précaution d'emploi
Le contrôle régulier de la fonction rénale et le strict respect des doses
sont impératifs.
Possibilité de survenue d’effets indésirables musculaires à
l’introduction d’une gliptine, malgré le traitement antérieur par
statine bien toléré.
GLOBULINES ANTILYMPHOCYTAIRES
(immunoglobuline de lapin anti-lymphocyte t humain, immunoglobulines equines antilymphocyte humain)
+ IMMUNOSUPPRESSEURS
A prendre en compteImmunodépression excessive avec risque de lymphoprolifération.
+ VACCINS VIVANTS ATTÉNUÉS
A prendre en compte
En particulier, utiliser un vaccin inactivé lorsqu'il existe (poliomyélite).
Risque de maladie généralisée éventuellement mortelle. Ce risque
est majoré chez les sujets âgés déjà immunodéprimés par la
maladie sous-jacente.
GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
(betamethasone, budesonide, cortisone, cortivazol, dexamethasone, methylprednisolone, prednisolone, prednisone, tetracosactide, triamcinolone)
+ ACIDE ACETYLSALICYLIQUE
ASDEC - APEC
Association déconseillée avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
A prendre en compte avec :
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour).
Majoration du risque hémorragique.
+ ANTICOAGULANTS ORAUX
Précaution d'emploi
Lorsque l'association est justifiée, renforcer la surveillance : le cas
échéant, avec les antivitamines K, contrôle biologique au 8e jour, puis
tous les 15 jours pendant la corticothérapie et après son arrêt.
Glucocorticoïdes (voies générale et rectale) : impact éventuel de la
corticothérapie sur le métabolisme de l'antivitamine K et sur celui
des facteurs de la coagulation. Risque hémorragique propre à la
corticothérapie (muqueuse digestive, fragilité vasculaire) à fortes
doses ou en traitement prolongé supérieur à 10 jours.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
A prendre en compteAugmentation du risque d’ulcération et d’hémorragie gastro-
intestinale.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ CURARES NON DÉPOLARISANTS
A prendre en compteAvec les glucocorticoïdes par voie IV : risque de myopathie sévère,
réversible après un délai éventuellement long (plusieurs mois).
+ FLUOROQUINOLONES
A prendre en comptePossible majoration du risque de tendinopathie, voire de rupture
tendineuse (exceptionnelle), particulièrement chez les patients
recevant une corticothérapie prolongée.
+ HÉPARINES
A prendre en compteAugmentation du risque hémorragique.
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie des
corticoïdes pendant le traitement par l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité des
corticoïdes par augmentation de leur métabolisme hépatique par
l'inducteur ; les conséquences sont particulièrement importantes
chez les addisoniens traités par l'hydrocortisone et en cas de
transplantation.
109
+ ISONIAZIDE
Précaution d'emploi
Surveillance clinique et biologique.
Décrit pour la prednisolone. Diminution des concentrations
plasmatiques de l'isoniazide. Mécanisme invoqué : augmentation
du métabolisme hépatique de l'isoniazide et diminution de celui des
glucocorticoïdes.
+ VACCINS VIVANTS ATTÉNUÉS
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt de la corticothérapie.
A l'exception des voies inhalées et locales, et pour des posologies
supérieures à 10 mg/j d’équivalent-prednisone (ou > 2 mg/kg/j chez
l’enfant ou > 20 mg/j chez l’enfant de plus de 10 kg) pendant plus
de deux semaines et pour les « bolus » de corticoïdes: risque de
maladie vaccinale généralisée éventuellement mortelle.
GLUCOCORTICOÏDES PAR VOIE INTRA-ARTICULAIRE ET MÉTABOLISÉS
(betamethasone, dexamethasone, méthylprednisolone, triamcinolone)
+ COBICISTAT
Précaution d'emploi
Préférer un corticoïde non CYP3A4-dépendant (hydrocortisone).
Décrit chez des patients HIV. Risque d’insuffisance surrénale
aiguë, même en cas d’injection unique. L’articulation peut
constituer un réservoir relarguant de façon continue le corticoïde
CYP3A4-dépendant dans la circulation générale, avec
augmentation possiblement très importante des concentrations du
corticoïde, à l’origine d’une freination de la réponse hypothalamo-
hypophysaire.
+ RITONAVIR
Précaution d'emploi
Préférer un corticoïde non CYP3A4-dépendant (hydrocortisone).
Décrit chez des patients HIV.
Risque d’insuffisance surrénale aiguë, même en cas d’injection
unique. L’articulation peut constituer un réservoir relarguant de
façon continue le corticoïde CYP3A4-dépendant dans la circulation
générale, avec augmentation possiblement très importante des
concentrations du corticoïde, à l’origine d’une freination de la
réponse hypothalamo-hypophysaire.
GLUCOSAMINE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adapation éventuelle de la posologie de
l’antivitamine K.
Augmentation du risque hémorragique.
GLYCEROL
+ LITHIUM
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
GRAZOPREVIR + ELBASVIR
(elbasvir, grazoprevir)
+ CICLOSPORINE
CONTRE-INDICATIONAugmentation des concentrations de grazoprévir et d’elbasvir.
+ ETRAVIRINE
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
grazoprevir/elbasvir par l’étravirine.
+ INDUCTEURS ENZYMATIQUES
CONTRE-INDICATIONRisque de diminution des concentrations de grazoprévir et
d’elbasvir par l’inducteur, avec possible retentissement sur
l’efficacité.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Précaution d'emploi
Surveillance clinique et biologique pendant l’association. La dose de
statine ne doit pas dépasser 20 mg par jour (10 mg avec la
rosuvastatine).
Augmentation des concentrations plasmatiques de
l’hypochlestérolémiant par augmentation de son absorption
intestinale.
+ INHIBITEURS PUISSANTS DU CYP3A4
CI - ASDEC
Contre-indication
- avec le ritonavir et le cobicistat
Association déconseillée
- avec les autres inhibiteurs du CYP3A4
Augmentation des concentrations plasmatiques de grazoprévir et
d’elbasvir.
110
+ SUNITINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Risque d’augmentation des effets indésirables du sunitinib par le
grazoprévir/elbasvir.
+ TACROLIMUS
Précaution d'emploi
Surveillance clinique et biologique étroite.
Augmentation des concentrations plasmatiques de tacrolimus par
inhibition de son métabolisme hépatique.
GRISEOFULVINE
Voir aussi : antabuse (réaction)
+ ESTROPROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de de la
griséofulvine.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par la
griséofulvine.
+ PROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode contraceptive fiable, additionnelle ou alternative,
pendant la durée de l'association et un cycle suivant.
Risque de diminution de l'efficacité du contraceptif hormonal par
augmentation de son métabolisme hépatique.
GUANETHIDINE
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATION
Interrompre le traitement par IMAO 15 jours avant le traitement par
guanéthidine.
Avec la guanéthidine utilisée par voie IV : risque de réactions
vasculaires imprévisibles, notamment d'hypotension.
HALOFANTRINE
Voir aussi : antiparasitaires susceptibles de donner des torsades de pointes - substances susceptibles de donner des torsades de pointes - substrats à risque du
CYP3A4
+ FLUCONAZOLE
Association DECONSEILLEE
Si cela est possible, interrompre le fluconazole. Si l'association ne peut
être évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si cela est possible, interrompre l'inhibiteur. Si l'association ne peut être
évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
+ JOSAMYCINE
Association DECONSEILLEE
Si cela est possible, interrompre le macrolide. Si l’association ne peut
être évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ STIRIPENTOL
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
HALOPERIDOL
Voir aussi : médicaments abaissant le seuil épileptogène - médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - neuroleptiques -
neuroleptiques antipsychotiques (sauf clozapine) - neuroleptiques susceptibles de donner des torsades de pointes - substances susceptibles de donner des torsades
de pointes
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique pendant le
traitement par l'halopéridol et après son arrêt.
Risque de moindre efficacité de l'halopéridol par
augmentation de son métabolisme hépatique par l'inducteur.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique pendant le
traitement par la rifampicine et après son arrêt.
Risque de diminution des concentrations plasmatiques de
l'halopéridol et de son efficacité thérapeutique, par augmentation
de son métabolisme hépatique par la rifampicine.
111
HALOTHANE
Voir aussi : anesthésiques volatils halogénés
+ BÊTA-2 MIMÉTIQUES
Association DECONSEILLEE
Interrompre le traitement par bêta-2 mimétiques si l'anesthésie doit se
faire sous halothane.
En cas d'intervention obstétricale, majoration de l'inertie utérine
avec risque hémorragique ; par ailleurs, troubles du rythme
ventriculaires graves, par augmentation de la réactivité cardiaque.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Association DECONSEILLEETroubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
HÉPARINES
(dalteparine sodique, danaparoide sodique, enoxaparine, fondaparinux, heparine calcique, heparine sodique, nadroparine calcique, reviparine, tinzaparine)
+ ANTIAGRÉGANTS PLAQUETTAIRES
A prendre en compteAugmentation du risque hémorragique.
+ ANTICOAGULANTS ORAUX
CI - PE
Les anticoagulants oraux d'action directe ne doivent pas être
administrés conjointement à l'héparine. Lors du relais de l'un par l'autre,
respecter l'intervalle entre les prises.
Lors du relais héparine/antivitamine K (nécessitant plusieurs jours),
renforcer la surveillance clinique et biologique.
Augmentation du risque hémorragique.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ DÉFIBROTIDE
Association DECONSEILLEERisque hémorragique accru.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
A prendre en compteAugmentation du risque hémorragique.
HÉPARINES (DOSES CURATIVES ET/OU SUJET ÂGÉ)
(dalteparine sodique, danaparoide sodique, enoxaparine, fondaparinux, heparine calcique, heparine sodique, nadroparine calcique, reviparine, tinzaparine)
+ ACIDE ACETYLSALICYLIQUE
ASDEC - APEC
Association déconseillée avec :
- des doses anti-inflammatoires d'acide acétylsalicylique (>=1g par prise
et/ou >=3g par jour)
- des doses antalgiques ou antipyrétiques (>=500 mg par prise et/ou
<3g par jour)
Utiliser un autre anti-inflammatoire ou un autre antalgique ou
antipyrétique.
A prendre en compte avec :
- des doses antiagrégantes (de 50 mg à 375 mg par jour).
Augmentation du risque hémorragique (inhibition de la fonction
plaquettaire et agression de la muqueuse gastroduodénale par
l’acide acétylsalicylique.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite.
Augmentation du risque hémorragique (agression de la muqueuse
gastroduodénale par les anti-inflammatoires non stéroïdiens).
+ DEXTRAN
Association DECONSEILLEEAugmentation du risque hémorragique (inhibition de la fonction
plaquettaire par le dextran 40).
+ THROMBOLYTIQUES
A prendre en compteAugmentation du risque hémorragique.
112
HÉPARINES (DOSES PRÉVENTIVES)
(dalteparine sodique, danaparoide sodique, enoxaparine, fondaparinux, heparine calcique, heparine sodique, nadroparine calcique, reviparine, tinzaparine)
+ ACIDE ACETYLSALICYLIQUE
A prendre en compteL’utilisation conjointe de médicaments agissant à divers niveaux de
l’hémostase majore le risque de saignement. Ainsi, chez le sujet de
moins de 65 ans, l’association de l'héparine à doses préventives,
ou de substances apparentées, à l’acide acétylsalicylique, quelle
que soit la dose, doit être prise en compte en maintenant une
surveillance clinique et éventuellement biologique.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
A prendre en compteAugmentation du risque hémorragique.
HORMONES THYROÏDIENNES
(levothyroxine, liothyronine sodique, thyroxines, tiratricol)
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
Précaution d'emploi
Contrôle clinique et biologique régulier, avec augmentation éventuelle
de la posologie des hormones thyroïdiennes.
Diminution probable de l'absorption des hormones thyroïdiennes,
par augmentation du pH intra-gastrique par l'antisécrétoire.
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium à distance des hormones thyroïdiennes
(plus de 2 heures, si possible).
Diminution de l’absorption digestive des hormones thyroïdiennes.
+ CHLOROQUINE
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
chloroquine et après son arrêt.
Risque d’hypothyroïdie clinique chez les patients substitués par
hormones thyroïdiennes.
+ EFAVIRENZ
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
l'inducteur et après son arrêt.
Risque d'hypothyroïdie clinique chez les patients hypothyroïdiens,
par augmentation du métabolisme de la T3 et de la T4.
+ ESTROGÈNES NON CONTRACEPTIFS
Précaution d'emploi
Surveillance clinique et biologique ; adaptation éventuelle des doses de
l'hormone thyroïdienne chez les femmes ménopausées prenant des
estrogènes.
Risque d'hypothyroïdie clinique en cas d'estrogénothérapie
substitutive.
+ FER
Précaution d'emploi
Prendre les hormones thyroïdiennes à distance du fer (plus de 2
heures, si possible).
Diminution de l'absorption digestive des hormones thyroïdiennes.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
l'inducteur et après son arrêt.
Risque d'hypothyroïdie clinique chez les patients hypothyroïdiens,
par augmentation du métabolisme de la T3 et de la T4.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique et biologique et adaptation éventuelle de la
posologie des hormones thyroïdiennes.
Risque de baisse de l’efficacité des hormones thyroïdiennes par
augmentation de leur métabolisme hépatique par le ritonavir.
+ MILLEPERTUIS
Association DECONSEILLEERisque de baisse de l’efficacité des hormones thyroïdiennes.
+ ORLISTAT
A prendre en compteRisque de déséquilibre du traitement thyroïdien substitutif en cas
de traitement par orlistat.
+ PROGUANIL
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
l’antipaludique et après son arrêt.
Risque d’hypothyroïdie clinique chez les patients substitués par
hormones thyroïdiennes.
113
+ RÉSINES CHÉLATRICES
Précaution d'emploi
Prendre les hormones thyroïdiennes à distance de la résine (plus de 2
heures, si possible).
Diminution de l'absorption digestive des hormones thyroïdiennes.
+ RIFABUTINE
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par la
rifabutine et après son arrêt.
Décrit pour la phénytoïne, la rifampicine, la carbamazépine. Risque
d'hypothyroïdie clinique chez les patients hypothyroïdiens, par
augmentation du métabolisme de la T3 et de la T4.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par la
rifampicine et après son arrêt.
Risque d'hypothyroïdie clinique chez les patients hypothyroïdiens,
par augmentation du métabolisme de la T3 et de la T4.
+ SELPERCATINIB
Précaution d'emploi
Surveillance clinique et biologique, et adjonction éventuelle de
liothyronine au traitement par la lévothyroxine.
Risque de moindre efficacité de la supplémentation en
lévothyroxine par baisse de la conversion de T4 en T3 en cas de
traitement par selpercatinib.
+ SUCRALFATE
Précaution d'emploi
Prendre les hormones thyroïdiennes à distance du sucralfate (plus de 2
heures, si possible).
Diminution de l'absorption digestive des hormones thyroïdiennes.
HUILES MINÉRALES
(paraffine, silicone)
+ PRÉSERVATIFS EN LATEX
CONTRE-INDICATION
Utiliser un lubrifiant hydrosoluble (glycérine, polyacrylamide...).
Risque de rupture du préservatif lors de l'utilisation avec des corps
gras ou des lubrifiants contenant des huiles minérales (huile de
paraffine, huile de silicone, etc...).
HYDROCORTISONE
Voir aussi : corticoïdes - hypokaliémiants
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie de
l'hydrocortisone pendant l'association et après l'arrêt de l'inducteur
enzymatique.
Risque de diminution de l'efficacité de l'hydrocortisone
(augmentation de son métabolisme) ; les conséquences sont
graves lorsque l'hydrocortisone est administrée en traitement
substitutif ou en cas de transplantation.
HYDROQUINIDINE
Voir aussi : antiarythmiques - antiarythmiques classe Ia - bradycardisants - substances susceptibles de donner des torsades de pointes - torsadogènes (sauf
arsénieux, antiparasitaires, neuroleptiques, méthadone...)
+ ALCALINISANTS URINAIRES
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations de l'hydroquinidine ; si besoin, adaptation de la
posologie pendant le traitement alcalinisant et après son arrêt.
Augmentation des concentrations plasmatiques de l'hydroquinidine
et risque de surdosage (diminution de l'excrétion rénale de
l'hydroquinidine par alcalinisation des urines).
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et ECG. En cas de réponse inattendue, contrôler
la digoxinémie et adapter la posologie.
Augmentation de la digoxinémie par diminution de la clairance
rénale de la digoxine. De plus, troubles de l'automatisme
(bradycardie excessive et troubles de la conduction auriculo-
ventriculaire).
+ ITRACONAZOLE
Précaution d'emploi
Surveillance des concentrations plasmatiques de l'antiarythmique et
diminution éventuelle de sa posologie si nécessaire.
Risque d'acouphènes et/ou de diminution de l'acuité auditive :
cinchonisme lié à une diminution du métabolisme hépatique de
l'antiarythmique par l'itraconazole.
HYDROXYCARBAMIDE
Voir aussi : cytotoxiques
+ VACCINS VIVANTS ATTÉNUÉS
Association DECONSEILLEE
L'association ne devra être envisagée que si les bénéfices sont estimés
comme étant supérieurs à ce risque.
S'il est décidé d’interrompre le traitement par hydroxycarbamide pour
effectuer la vaccination, un délai de 3 mois après l’arrêt est
recommandé.
Dans son indication chez le patient drépanocytaire, risque
théorique de maladie vaccinale généralisée.
114
HYDROXYCHLOROQUINE
Voir aussi : substances susceptibles de donner des torsades de pointes
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
HYPERKALIÉMIANTS
Certains médicaments ou classes thérapeutiques sont susceptibles de favoriser la survenue d'une hyperkaliémie : les sels de potassium, les diurétiques
hyperkaliémiants, les inhibiteurs de l'enzyme de conversion, les antagonistes de l'angiotensine II, les anti-inflammatoires non stéroïdiens, les héparines (de bas poids
moléculaire ou non fractionnées), les immunosuppresseurs comme la ciclosporine ou le tacrolimus, le triméthoprime.
L’association de ces médicaments majore le risque d’hyperkaliémie. Ce risque est particulièrement important avec les diurétiques épargneurs de potassium,
notamment lorsqu’ils sont associés entre eux ou avec des sels de potassium, tandis que l’association d’un IEC et d’un AINS, par exemple, est à moindre risque dès
l’instant que sont mises en œuvre les précautions recommandées.
Pour connaître les risques et les niveaux de contrainte spécifiques aux médicaments hyperkaliémiants, il convient de se reporter aux interactions propres à chaque
substance.
Toutefois, certaines substances, comme le triméthoprime, ne font pas l’objet d’interactions spécifiques au regard de ce risque. Néanmoins, ils peuvent agir comme
facteurs favorisants lorsqu’ils sont associés à d’autres médicaments déjà mentionnés dans ce chapeau.
(aceclofenac, acide mefenamique, acide niflumique, acide tiaprofenique, alminoprofene, amiloride, azilsartan, benazepril, candesartan cilexetil, canrenoate de
potassium, captopril, celecoxib, ciclosporine, cilazapril, dalteparine sodique, danaparoide sodique, dexketoprofene trometamol, diclofenac, drospirenone, enalapril,
enoxaparine, eplerenone, eprosartan, etodolac, fenoprofene, flurbiprofene, fondaparinux, fosinopril, heparine calcique, heparine sodique, ibuprofene, indometacine,
irbesartan, ketoprofene, lisinopril, losartan, meloxicam, moexipril, morniflumate, nabumetone, nadroparine calcique, naproxene, nimesulide, olmesartan, parecoxib,
périndopril, piroxicam, piroxicam-betadex, potassium, quinapril, ramipril, reviparine, rofecoxib, spironolactone, sulindac, tacrolimus, telmisartan, tenoxicam, tinzaparine,
trandolapril, triamterene, trimethoprime, valsartan, zofenopril)
+ AUTRES HYPERKALIÉMIANTS
A prendre en compteRisque de majoration de l’hyperkaliémie, potentiellement létale.
HYPNOTIQUES
Les hypnotiques actuellement prescrits sont soit des benzodiazépines et apparentés (zolpidem, zopiclone), soit des antihistaminiques H1. Outre une majoration de la
sédation lorsqu’il sont prescrits avec d’autres médicaments dépresseurs du SNC, ou en cas de consommation alcoolique, il faut prendre en compte également, pour
les benzodiazépines, la possibilité de majoration de l’effet dépresseur respiratoire lorsqu’elles sont associées avec des morphinomimétiques, d’autres
benzodiazépines, ou du phénobarbital, et cela notamment chez le sujet âgé.
Se reporter à "médicaments sédatifs" (benzodiazépines et apparentés, antihistaminiques H1 sédatifs).
(alimemazine, doxylamine, estazolam, eszopiclone, loprazolam, lormetazepam, nitrazepam, promethazine, zolpidem, zopiclone)
+ AUTRES HYPNOTIQUES
A prendre en compteMajoration de la dépression centrale.
HYPOKALIÉMIANTS
L'hypokaliémie est un facteur favorisant l'apparition de troubles du rythme cardiaque (torsades de pointes, notamment) et augmentant la toxicité de certains
médicaments, par exemple la digoxine. De ce fait, les médicaments qui peuvent entraîner une hypokaliémie sont impliqués dans un grand nombre d'interactions. Il
s'agit des diurétiques hypokaliémiants, seuls ou associés, des laxatifs stimulants, des glucocorticoïdes, du tétracosactide et de l'amphotéricine B (voie IV).
(altizide, amphotericine b, bendroflumethiazide, betamethasone, bisacodyl, boldo, bourdaine, bumetanide, cascara, cascara sagrada, chlortalidone, cicletanine,
clopamide, cortisone, cortivazol, dexamethasone, fludrocortisone, furosemide, hydrochlorothiazide, hydrocortisone, indapamide, methyclothiazide, methylprednisolone,
piretanide, prednisolone, prednisone, reglisse, rhubarbe, ricin, ricinus communis, sene, sene de l'inde, sodium (docusate de), sodium (picosulfate de), sodium
(ricinoleate de), tetracosactide, triamcinolone)
+ AUTRES HYPOKALIÉMIANTS
Précaution d'emploi
Surveillance de la kaliémie avec si besoin correction.
Risque majoré d'hypokaliémie.
+ DIGOXINE
Précaution d'emploi
Corriger auparavant toute hypokaliémie et réaliser une surveillance
clinique, électrolytique et électrocardiographique.
Hypokaliémie favorisant les effets toxiques des digitaliques.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Corriger toute hypokaliémie avant d’administrer le produit et réaliser une
surveillance clinique, électrolytique et électrocardiographique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
115
HYPONATRÉMIANTS
Certains médicaments sont plus fréquemment impliqués dans la survenue d’une hyponatrémie. Ce sont les diurétiques, la desmopressine, les antidépresseurs
inhibant la recapture de la sérotonine, la carbamazépine et l’oxcarbazépine. L’association de ces médicaments majore le risque d’hyponatrémie.
(altizide, amiloride, argipressine, bendroflumethiazide, bumetanide, canrenoate de potassium, carbamazepine, chlortalidone, cicletanine, citalopram, clopamide,
desmopressine, eplerenone, escitalopram, fluoxetine, fluvoxamine, furosemide, hydrochlorothiazide, indapamide, methyclothiazide, oxcarbazepine, paroxetine,
piretanide, sertraline, spironolactone, triamterene)
+ AUTRES MÉDICAMENTS HYPONATRÉMIANTS
A prendre en compteMajoration du risque d’hyponatrémie.
IBRUTINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés - substrats à risque du CYP3A4
+ AMIODARONE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d'augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par l’amiodarone.
+ ANTIAGRÉGANTS PLAQUETTAIRES
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ ANTICOAGULANTS ORAUX
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite (pour les antivitamines K, contrôle plus fréquent de l’INR).
Augmentation du risque hémorragique.
+ CRIZOTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le crizotinib.
+ DILTIAZEM
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d'augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le diltiazem.
+ DRONEDARONE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par la dronédarone.
+ FLUCONAZOLE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le fluconazole.
+ IMATINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par l'imatinib.
+ VERAPAMIL
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le vérapamil.
IDÉLALISIB
+ ANTAGONISTES DES CANAUX CALCIQUES
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’antagoniste
calcique pendant le traitement par l’idélalisib et après son arrêt.
Majoration des effets indésirables de l’antagoniste des canaux
calciques, à type d’hypotension orthostatique, notamment chez le
sujet âgé.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques d’idélalisib par
augmentation de son métabolisme hépatique par l'inducteur
enzymatique.
116
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en compteAugmentation des concentrations plasmatiques d’idélalisib par
diminution de son métabolisme hépatique par l’inhibiteur.
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution importante des concentrations plasmatiques
d’idélalisib par augmentation de son métabolisme hépatique par le
millepertuis.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques d’idélalisib par
augmentation de son métabolisme hépatique par l’inducteur.
+ SUBSTRATS À RISQUE DU CYP3A4
Association DECONSEILLEEAugmentation des concentrations plasmatiques du substrat par
diminution de son métabolisme hépatique par l’idelalisib.
IFOSFAMIDE
Voir aussi : cytotoxiques - médicaments néphrotoxiques
+ APREPITANT
A prendre en compteRisque d’augmentation de la neurotoxicité de l’ifosfamide.
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
Association DECONSEILLEERisque de majoration de la neurotoxicité de l'ifosfamide par
augmentation de son métabolisme hépatique par le phénobarbital.
+ VÉMURAFÉNIB
A prendre en compteRisque de diminution des concentrations de l'ifosfamide, avec
augmentation de son métabolite actif et toxicité majorée.
IMAO IRRÉVERSIBLES
(iproniazide, phénelzine)
+ ADRÉNALINE (VOIE BUCCO-DENTAIRE OU SOUS-CUTANÉE)
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ ALCOOL (BOISSON OU EXCIPIENT)
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Majoration des effets hypertenseurs et/ou hyperthermiques de la
tyramine présente dans certaines boissons alcoolisées (chianti,
certaines bières, etc).
+ DEXTROMETHORPHANE
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ GUANETHIDINE
CONTRE-INDICATION
Interrompre le traitement par IMAO 15 jours avant le traitement par
guanéthidine.
Avec la guanéthidine utilisée par voie IV : risque de réactions
vasculaires imprévisibles, notamment d'hypotension.
+ INHIBITEURS DE LA CATÉCHOL-O-MÉTHYLTRANSFÉRASE (COMT)
CONTRE-INDICATIONPotentialisation des effets pharmacologiques, et notamment
vasopresseurs, des catécholamines par inhibition conjuguée de
leur métabolisme.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
CONTRE-INDICATION
Respecter un délai de deux semaines entre l'arrêt de l'IMAO et le début
du traitement par l'antidépresseur sérotoninergique, et d'au moins une
semaine entre l'arrêt de l'antidépresseur sérotoninergique (sauf pour la
fluoxétine : cinq semaines) et le début.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
117
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
CONTRE-INDICATION
Respecter un délai de deux semaines entre l'arrêt de l'IMAO et le début
de l'autre traitement, et d'au moins une semaine entre l'arrêt de l'autre
traitement et le début de l'IMAO.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ MIDODRINE
CONTRE-INDICATIONCrises hypertensives (inhibition du métabolisme des amines
pressives). Du fait de la durée d'action des IMAO, cette interaction
est encore possible 15 jours après l'arrêt de l'IMAO.
+ MILLEPERTUIS
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ PETHIDINE
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ RESERPINE
CONTRE-INDICATIONAgitation psychomotrice, convulsions, hypertension.
+ SYMPATHOMIMÉTIQUES ALPHA (VOIES ORALE ET/OU NASALE)
Association DECONSEILLEECrises hypertensives (inhibition du métabolisme des amines
pressives). Du fait de la durée d'action de l'IMAO, cette interaction
est encore possible 15 jours après l'arrêt de l'IMAO.
+ SYMPATHOMIMÉTIQUES ALPHA ET BÊTA (VOIE IM ET IV)
Précaution d'emploi
A n'utiliser que sous contrôle médical strict.
Augmentation de l'action pressive du sympathomimétique, le plus
souvent modérée.
+ SYMPATHOMIMÉTIQUES INDIRECTS
CONTRE-INDICATIONHypertension paroxystique, hyperthermie pouvant être fatale. Du
fait de la durée d'action de l'IMAO, cette interaction est encore
possible 15 jours après l'arrêt de l'IMAO.
+ TETRABENAZINE
CONTRE-INDICATIONRisque de crises hypertensives. Du fait de la durée d'action de
l'IMAO, cette interaction est encore théoriquement possible 15 jours
après son arrêt.
+ TIANEPTINE
Association DECONSEILLEERisque de collapsus, hypertension paroxystique, hyperthermie,
convulsions, décès.
+ TRAMADOL
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
sueurs, tremblements, confusion, voire coma.
+ TRIPTANS MÉTABOLISÉS PAR LA MAO
CONTRE-INDICATIONRisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ TRIPTANS NON MÉTABOLISÉS PAR LA MAO
Association DECONSEILLEERisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
(bleu de methylene, linezolide, moclobemide, tédizolide)
+ DEXTROMETHORPHANE
Association DECONSEILLEERisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
118
+ IMAO-B
CONTRE-INDICATIONRisque de poussée hypertensive, par absence de sélectivité sur la
monoamine oxydase, notamment en cas d’alimentation riche en
tyramine (fromage, bière,…).
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique très étroite.
Débuter l'association aux posologies minimales recommandées.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique très étroite.
Débuter l'association aux posologies minimales recommandées.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueur, confusion voire coma.
+ MILLEPERTUIS
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ PETHIDINE
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ SYMPATHOMIMÉTIQUES ALPHA ET BÊTA (VOIE IM ET IV)
Précaution d'emploi
A n'utiliser que sous contrôle médical strict.
Par extrapolation à partir des IMAO non sélectifs : risque
d'augmentation de l'action pressive.
+ SYMPATHOMIMÉTIQUES INDIRECTS
CI - ASDEC
Contre-indication :
avec le bupropion
Association déconseillée :
avec les autres sympathomimétiques indirects
Risque de vasoconstriction et/ou de poussées hypertensives.
+ TRAMADOL
Association DECONSEILLEERisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ TRIPTANS MÉTABOLISÉS PAR LA MAO
CONTRE-INDICATIONRisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ TRIPTANS NON MÉTABOLISÉS PAR LA MAO
Association DECONSEILLEERisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
IMAO-B
(rasagiline, safinamide, selegiline)
+ BUPROPION
CONTRE-INDICATIONRisque de crises hypertensives.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
CONTRE-INDICATIONRisque de poussée hypertensive, par absence de sélectivité sur la
monoamine oxydase, notamment en cas d’alimentation riche en
tyramine (fromage, bière,…).
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteRisque d'apparition d'un syndrome sérotoninergique.
+ LEVODOPA
A prendre en compteAugmentation du risque d'hypotension orthostatique.
119
+ PETHIDINE
CONTRE-INDICATIONManifestations d'excitation centrale évoquant un syndrome
sérotoninergique : diarrhée, tachycardie, sueurs, tremblements,
confusion voire coma.
+ TRAMADOL
A prendre en compteRisque d’apparition d’un syndrome sérotoninergique.
+ TRIPTANS MÉTABOLISÉS PAR LA MAO
CONTRE-INDICATIONRisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ TRIPTANS NON MÉTABOLISÉS PAR LA MAO
Association DECONSEILLEERisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
IMATINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés - médicaments à l'origine d'atteintes musculaires - substrats à risque du CYP3A4
+ ANTICOAGULANTS ORAUX
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite (pour les antivitamines K, contrôle plus fréquent de l’INR).
Augmentation du risque hémorragique.
Pour l’apixaban et le rivaroxaban, risque de diminution de leur
métabolisme par l’imatinib, se surajoutant au risque
pharmacodynamique.
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par l'imatinib.
+ TÉDIZOLIDE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de
l'imatinib, par augmentation de son absorption avec le tédizolide
administré par voie orale.
IMMUNOSUPPRESSEURS
(ciclosporine, everolimus, sirolimus, tacrolimus, temsirolimus)
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations des
immunosuppresseurs, et perte d‘efficacité, par augmentation de
leur métabolisme hépatique par l’apalutamide.
+ CLARITHROMYCINE
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ CYTOTOXIQUES
A prendre en compteImmunodépression excessive avec risque de syndrome lympho-
prolifératif.
+ DALFOPRISTINE
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ DILTIAZEM
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par diminution de son métabolisme.
+ DRONEDARONE
Association DECONSEILLEEAugmentation importante des concentrations sanguines de
l’immunosuppresseur par diminution de son métabolisme.
120
+ ERYTHROMYCINE
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ FLUCONAZOLE
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de sa posologie pendant
l'association et après son arrêt.
Risque d'augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme et de la
créatininémie.
+ FLUCYTOSINE
A prendre en compteRisque de majoration de la toxicité hématologique.
+ GLOBULINES ANTILYMPHOCYTAIRES
A prendre en compteImmunodépression excessive avec risque de lymphoprolifération.
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Augmentation de la posologie de l'immunosuppresseur sous contrôle
des concentrations sanguines. Réduction de la posologie après l'arrêt
de l'inducteur.
Diminution des concentrations sanguines et de l'efficacité de
l'immunosuppresseur, par augmentation de son métabolisme
hépatique par l'inducteur.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation de sa
posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ ITRACONAZOLE
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ KETOCONAZOLE
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ LÉTERMOVIR
Précaution d'emploi
Surveillance clinique et biologique renforcée.
Augmentation, éventuellement très importante, des concentrations
sanguines de l'immunosuppresseur par inhibition de son
métabolisme et de la créatininémie.
+ MARIBAVIR
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation éventuelle de la posologie
pendant l'association et après son arrêt.
Possible augmentation des concentrations de
l’immunosuppresseur.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations sanguines de l'immunosuppresseur,
en raison de l'effet inducteur enzymatique du millepertuis, avec
risque de baisse d'efficacité voire d'annulation de l'effet dont les
conséquences peuvent être éventuellement graves (rejet de greffe).
+ NICARDIPINE
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de sa posologie pendant le
traitement et après l'arrêt.
Augmentation des concentrations sanguines de
l'immunodépresseur, par inhibition de son métabolisme.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation de la biodisponibilité de l’immunosuppresseur et par
conséquent de ses effets indésirables.
+ POSACONAZOLE
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
121
+ PRISTINAMYCINE
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de sa posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ QUINUPRISTINE
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ RANOLAZINE
Précaution d'emploi
Surveillance clinique et biologique, et adaptation éventuelle de la
posologie de l’immunosuppresseur.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme par la
ranolazine.
+ STIRIPENTOL
CONTRE-INDICATIONAugmentation des concentrations sanguines de
l’immunosuppresseur (diminution de son métabolisme hépatique).
+ TELITHROMYCINE
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ VACCINS VIVANTS ATTÉNUÉS
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
+ VÉMURAFÉNIB
Association DECONSEILLEERisque de diminution des concentrations des
immunosuppresseurs, avec pour conséquence un risque
d’inefficacité.
+ VORICONAZOLE
ASDEC - PE
Association déconseillée
- avec l'évérolimus, le sirolimus, et le temsirolimus.
Précaution d'emploi
- avec la ciclosporine et le tacrolimus :
dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique
par le voriconazole.
INDUCTEURS ENZYMATIQUES
Certains médicaments ont la propriété d'activer considérablement certaines voies métaboliques hépatiques par induction enzymatique. Associés à des médicaments
fortement métabolisés au niveau du foie, ils sont, de ce fait, en mesure d'en modifier les concentrations plasmatiques. Il peut s'ensuivre, dans la majorité des cas, une
moindre activité des médicaments associés à l'inducteur, voire la formation de métabolites toxiques.
Les inducteurs enzymatiques à l'origine d'interactions cliniquement pertinentes sont notamment représentés par certains antiépileptiques, certains antituberculeux et
antirétroviraux et le millepertuis (pour ce dernier, se reporter aux interactions qui lui sont propres).
Les médicaments dont l'efficacité peut être altérée sont nombreux : immunosuppresseurs, estroprogestatifs et progestatifs, inhibiteurs de protéase, anticoagulants
oraux, glucocorticoïdes, hormones thyroïdiennes, antagonistes du calcium, isoniazide, théophylline, etc…
(apalutamide, carbamazepine, cénobamate, dabrafénib, efavirenz, enzalutamide, eslicarbazépine, fosphenytoine, létermovir, lorlatinib, lumacaftor, nevirapine,
oxcarbazepine, phenobarbital, phenytoine, pitolisant, primidone, rifabutine, rifampicine, sotorasib)
+ ANDROGÈNES
Précaution d'emploi
Surveillance clinique et biologique pendant l’association et 1 à 2
semaines après l’arrêt de l’inducteur.
Risque de diminution des concentrations plasmatiques de
l'androgène et par conséquent de son efficacité, par augmentation
de son métabolisme hépatique par l’inducteur.
+ APRÉMILAST
Association DECONSEILLEEDiminution des concentrations plasmatiques d’aprémilast par
augmentatiion de son métabolisme par l’inducteur.
+ ARIPIPRAZOLE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
l’aripiprazole pendant l’association et 1 à 2 semaines après l’arrêt de
l’inducteur.
Diminution des concentrations plasmatiques de l’aripiprazole.
122
+ BAZÉDOXIFÈNE
Précaution d'emploi
Surveillance d'éventuels signes évocateurs d’une perte d’efficacité
(saignements).
Diminution des concentrations plasmatiques de bazédoxifène par
l’inducteur.
+ BÉDAQUILINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de bédaquiline par
augmentation de son métabolisme par l’inducteur.
+ BICTÉGRAVIR
CI - ASDEC
Contre-indication :
- avec la rifampicine
Association déconseillée :
- avec les autres inducteurs enzymatiques
Risque de perte d’efficacité par diminution, éventuellement
importante, des concentrations de bictégravir.
+ BORTEZOMIB
A prendre en compteDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
+ CABAZITAXEL
A prendre en compteDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
+ CABOTEGRAVIR
CI - APEC
Contre-indication :
- avec la rifampicine, la carbamazépine, l'oxcarbazépine, la phénytoïne,
le phénobarbital
A prendre en compte :
- avec les autres inducteurs
Diminution importante des concentrations de cabotégravir avec la
rifampicine, avec risque de réduction de la réponse virologique.
+ CASPOFUNGINE
Précaution d'emploi
En cas de traitement par inducteur, maintenir la posologie à 70 mg par
jour dès le 2e jour.
Diminution des concentrations plasmatiques de caspofungine.
+ CYCLOPHOSPHAMIDE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
métabolite actif du cyclophosphamide par l'inducteur, et donc de sa
toxicité.
+ CYPROTERONE
ASDEC - PE
Association déconseillée:
- dans son utilisation comme contraceptif hormonal: utiliser de
préférence une autre méthode de contraception en particulier de type
mécanique, pendant la durée de l'association et un cycle suivant.
Précaution d'emploi
- dans ses indications comme anti-androgène: surveillance clinique et
adaptation éventuelle de la posologie de la cyprotérone pendant
l'association et après son arrêt.
Risque de diminution de l'efficacité de la cyprotérone.
+ DASABUVIR
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques du
dasabuvir par l’inducteur.
+ DISOPYRAMIDE
Précaution d'emploi
Surveillance clinique et éventuellement adaptation de la posologie du
disopyramide pendant l’association et 1 à 2 semaines après l’arrêt de
l’inducteur.
Risque de diminution des concentrations du disopyramide par
l’inducteur.
+ DOCETAXEL
Association DECONSEILLEEDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
123
+ DOLUTÉGRAVIR
ASDEC - PE
Association déconseillée :
- en cas de résistance à la classe des inhibiteurs d'intégrase
Précaution d'emploi :
- en l'absence de résistance à la classe des inhibiteurs d'intégrase
Adaptation de la posologie de dolutégravir à 50 mg 2 fois par jour
pendant l’association et une semaine après son arrêt.
Diminution des concentrations plasmatiques de dolutégravir par
augmentation de son métabolisme par l’inducteur.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt de
l’inducteur.
Diminution de l'efficacité contraceptive, par augmentation du
métabolisme hépatique du contraceptif hormonal par l'inducteur.
+ ETOPOSIDE
Association DECONSEILLEE
Si l'association s'avère nécessaire, surveillance clinique et adaptation
éventuelle de la posologie d’étoposide pendant l’association, et 1 à 2
semaines après l’arrêt de l’inducteur.
Diminution des concentrations plasmatiques d’étoposide par
l’inducteur.
+ FOSTEMSAVIR
CI - APEC
Contre-indication :
- avec la rifampicine, la carbamazépine, la phénytoïne, l’enzalutamide
A prendre en compte :
- avec les autres inducteurs
Diminution significative des concentrations de fotemsavir avec la
rifampicine, avec risque de réduction de la réponse virologique.
+ GLASDÉGIB
ASDEC - PE
Association déconseillée
- avec la rifampicine
- avec les anticonvulsivants inducteurs enzymatiques (carbamazépine,
phénytoïne, phénobarbital…)
Précaution d'emploi
- avec les autres inducteurs
- si l’association ne peut être évitée, augmenter la dose de glasdégib.
Diminution, éventuellement importante selon l'inducteur, des
concentrations de glasdégib par augmentation de son
métabolisme, avec risque d'inefficacité.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie des
corticoïdes pendant le traitement par l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité des
corticoïdes par augmentation de leur métabolisme hépatique par
l'inducteur ; les conséquences sont particulièrement importantes
chez les addisoniens traités par l'hydrocortisone et en cas de
transplantation.
+ GRAZOPREVIR + ELBASVIR
CONTRE-INDICATIONRisque de diminution des concentrations de grazoprévir et
d’elbasvir par l’inducteur, avec possible retentissement sur
l’efficacité.
+ HYDROCORTISONE
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie de
l'hydrocortisone pendant l'association et après l'arrêt de l'inducteur
enzymatique.
Risque de diminution de l'efficacité de l'hydrocortisone
(augmentation de son métabolisme) ; les conséquences sont
graves lorsque l'hydrocortisone est administrée en traitement
substitutif ou en cas de transplantation.
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Augmentation de la posologie de l'immunosuppresseur sous contrôle
des concentrations sanguines. Réduction de la posologie après l'arrêt
de l'inducteur.
Diminution des concentrations sanguines et de l'efficacité de
l'immunosuppresseur, par augmentation de son métabolisme
hépatique par l'inducteur.
+ IRINOTECAN
Association DECONSEILLEEDiminution probable des concentrations plasmatiques du
métabolite actif de l'irinotécan, avec risque d'échec du traitement
cytotoxique.
+ ISAVUCONAZOLE
CONTRE-INDICATIONDiminution des concentrations plasmatiques d’isavuconazole par
augmentation de son métabolisme hépatique par l’inducteur.
+ ITRACONAZOLE
Association DECONSEILLEEDiminution des concentrations plasmatiques d’itraconazole, avec
risque de perte d’efficacité, par augmentation de son métabolisme
hépatique par l’inducteur.
124
+ IVACAFTOR (SEUL OU ASSOCIÉ)
Association DECONSEILLEEDiminution importante des concentrations de l’ivacaftor, avec
risque de perte d’efficacité.
+ LEVONORGESTREL
Précaution d'emploi
En cas de prise d’un médicament inducteur dans les 4 dernières
semaines, l’utilisation d’une contraception d’urgence non hormonale
(DIU au cuivre) devrait s’envisager.
Si ce n’est pas possible, le doublement de la dose de lévonorgestrel est
une autre option.
Avec le lévonorgestrel utilisé dans l’indication contraception
d’urgence, diminution importante des concentrations plasmatiques
de lévonorgestrel, avec risque d’inefficacité.
+ LURASIDONE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la lurasidone par
augmentation de son métabolisme hépatique par l’inducteur.
+ MACITENTAN
Association DECONSEILLEEDiminution des concentrations plasmatiques de macitentan par
augmentation de son métabolisme par l’inducteur.
+ MARAVIROC
Précaution d'emploi
La dose de maraviroc doit être augmentée à 600 mg deux fois par jour
dans cette situation.
En l’absence de co-administration avec un inhibiteur puissant du
CYP3A4, diminution des concentrations de maraviroc par
l’inducteur (sauf la névirapine).
+ MARIBAVIR
Association DECONSEILLEE
Si l’association ne peut être évitée, augmentation éventuelle de la
posologie de maribavir.
Diminution possiblement importante des concentrations de
maribavir avec la rifampicine, avec risque de réduction de la
réponse virologique.
+ METHADONE
Précaution d'emploi
Augmenter la fréquence des prises de méthadone (2 à 3 fois par jour au
lieu d'une fois par jour).
Diminution des concentrations plasmatiques de méthadone avec
risque d'apparition d'un syndrome de sevrage, par augmentation de
son métabolisme hépatique.
+ MIANSERINE
Association DECONSEILLEERisque d’inefficacité de la miansérine.
+ MIDOSTAURINE
CONTRE-INDICATIONDiminution des concentrations de midostaurine par l’inducteur
enzymatique.
+ NALOXEGOL
Association DECONSEILLEEDiminution des concentrations de naloxegol par l’inducteur.
+ NÉTUPITANT
Association DECONSEILLEEDiminution très importante des concentrations de nétupitant avec
risque de perte d'efficacité.
+ OLAPARIB
Association DECONSEILLEEDiminution, éventuellement très importante selon l’inducteur, des
concentrations plasmatiques de l’olaparib par augmentation de son
métabolisme hépatique par l’inducteur.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la bithérapie par
augmentation de son métabolisme hépatique par l’inducteur.
+ OXYCODONE
Association DECONSEILLEE
Adaptation éventuelle de la posologie d’oxycodone .
Diminution des concentrations plasmatiques de l’oxycodone par
augmentation de son métabolisme par l’inducteur.
125
+ PACLITAXEL
Association DECONSEILLEEDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
+ PROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique, pendant la durée de l'association et un cycle
suivant.
Diminution de l'efficacité contraceptive du contraceptif hormonal,
par augmentation de son métabolisme hépatique par l'inducteur.
+ PROGESTATIFS NON CONTRACEPTIFS, ASSOCIÉS OU NON À UN ESTROGÈNE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant l'administration de l'inducteur et après son
arrêt.
Diminution de l'efficacité du progestatif.
+ RÉGORAFÉNIB
Association DECONSEILLEEDiminution des concentrations plasmatiques de régorafenib par
augmentation de son métabolisme par l’inducteur.
+ RILPIVIRINE
CONTRE-INDICATIONDiminution significative des concentrations plasmatiques de
rilpivirine par augmentation de son métabolisme hépatique par
l’inducteur.
+ ROLAPITANT
Association DECONSEILLEEDiminution très importante des concentrations de rolapitant avec
risque de perte d’efficacité.
+ SERTRALINE
Association DECONSEILLEERisque d’inefficacité du traitement antidépresseur.
+ SOFOSBUVIR
CI - ASDEC
Contre-indication :
- avec la rifampicine
- avec les anticonvulsivants inducteurs enzymatiques
Association déconseillée:
- avec les autres inducteurs.
Risque de diminution des concentrations plasmatiques de
sofosbuvir par diminution de son absorption intestinale par
l’inducteur.
+ TAMOXIFENE
A prendre en compteRisque d’inefficacité du tamoxifène par augmentation de son
métabolisme par l’inducteur.
+ TÉNOFOVIR ALAFÉNAMIDE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique pendant
l’association et 1 à 2 semaines après l’arrêt de l’inducteur.
Diminution des concentrations plasmatiques du ténofovir
alafénamide par diminution de son absorption par l’inducteur.
+ VÉMURAFÉNIB
Association DECONSEILLEERisque de diminution des concentrations du vémurafénib, avec
moindre efficacité.
+ VÉNÉTOCLAX
Association DECONSEILLEEDiminution importante des concentrations de vénétoclax, avec
risque de perte d’efficacité.
+ VINCA-ALCALOÏDES CYTOTOXIQUES
Association DECONSEILLEEDiminution des concentrations plasmatiques du vinca-alcaloïde par
l’inducteur, avec possible retentissement sur l’efficacité..
+ VISMODÉGIB
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
vismodegib par augmentation de son métabolisme hépatique par
l’inducteur.
126
INDUCTEURS ENZYMATIQUES PUISSANTS
(apalutamide, carbamazepine, enzalutamide, fosphenytoine, phenobarbital, phenytoine, primidone)
+ ABIRATERONE
Association DECONSEILLEEDiminution notable des concentrations plasmatiques de
l’abiratérone, avec risque de moindre efficacité.
+ AFATINIB
Précaution d'emploi
Surveillance clinique pendant l’association et 1 à 2 semaines après leur
arrêt.
Diminution des concentrations plasmatiques de l’afatinib par
augmentation de son métabolisme par ces substances.
+ ALBENDAZOLE
Précaution d'emploi
Surveillance clinique de la réponse thérapeutique et adaptation
éventuelle de la posologie de l’albendazole pendant le traitement avec
l’inducteur enzymatique et après son arrêt.
Diminution importante des concentrations plasmatiques de
l’albendazole et de son métabolite actif par l’inducteur, avec risque
de baisse de son efficacité.
+ ANTAGONISTES DES CANAUX CALCIQUES
ASDEC - PE
Association déconseillée avec la nimodipine
Précaution d'emploi :
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par l'inducteur et après
son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique.
+ ANTIARYTHMIQUES CLASSE IA
Précaution d'emploi
Surveillance clinique, ECG et contrôle des concentrations plasmatiques
; si besoin, adaptation de la posologie de l'antiarythmique pendant le
traitement par l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de
l'antiarythmique, par augmentation de son métabolisme hépatique
par l'inducteur.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'anticonvulsivant inducteur
et 8 jours après son arrêt.
Diminution (ou, rarement, augmentation avec la phénytoïne) de
l'effet de l'antivitamine K par augmentation de son métabolisme
hépatique par l'anticonvulsivant inducteur.
+ APIXABAN
Association DECONSEILLEEDiminution des concentrations plasmatiques de l’apixaban par
l'inducteur enzymatique, avec risque de réduction de l’effet
thérapeutique.
+ APREPITANT
Association DECONSEILLEERisque de diminution très importante des concentrations
d'aprépitant.
+ BOSENTAN
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
+ CANNABIDIOL
Association DECONSEILLEEDiminution des concentrations plasmatiques de cannabidiol avec
risque de perte d’efficacité.
+ CLOZAPINE
ASDEC - PE
Association déconseillée:
- avec la carbamazépine, l'apalutamide, l'enzalutamide
Précaution d'emploi:
- Avec la phénytoïne, la fosphénytoïne, la primidone, le phénobarbital.
Surveillance clinique et adaptation posologique de la clozapine pendant
l’association et après l’arrêt de l’inducteur
- Avec l'apalutamide, l'enzalutamide : risque vraisemblablement modéré
Diminution des concentrations plasmatiques de clozapine avec
risque de perte d’efficacité.
De plus, avec la carbamazépine, risque de majoration des effets
hématologiques graves.
+ COBICISTAT
CONTRE-INDICATIONRisque de diminution de l’efficacité du cobicistat par augmentation
de son métabolisme par l’inducteur.
127
+ DABIGATRAN
Association DECONSEILLEEDiminution des concentrations plasmatiques de dabigatran, avec
risque de diminution de l'effet thérapeutique.
+ DAROLUTAMIDE
Association DECONSEILLEEDiminution des concentrations plasmatiques de dalorutamide avec
risque de perte d’efficacité.
+ DEFERASIROX
Précaution d'emploi
Surveiller la ferritinémie pendant et après le traitement par l’inducteur
enzymatique. Si besoin, adaptation de la posologie de déférasirox.
Risque de diminution des concentrations plasmatiques de
déférasirox.
+ DÉLAMANID
CONTRE-INDICATIONDiminution des concentrations plasmatiques de delamanid par
augmentation de son métabolisme hépatique par l’inducteur.
+ DOXYCYCLINE
A prendre en compteRisque de diminution importante des concentrations de doxycycline.
+ DRONEDARONE
Association DECONSEILLEEDiminution importante des concentrations de dronédarone par
augmentation de son métabolisme, sans modification notable du
métabolite actif.
+ ESTROGÈNES NON CONTRACEPTIFS
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant l'administration de l'inducteur et après son
arrêt.
Diminution de l'efficacité de l'estrogène.
+ FENTANYL
Association DECONSEILLEE
Préférer un autre morphinique.
Diminution des concentrations plasmatiques de fentanyl par
augmentation de son métabolisme hépatique par l'inducteur.
+ HALOPERIDOL
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique pendant le
traitement par l'halopéridol et après son arrêt.
Risque de moindre efficacité de l'halopéridol par
augmentation de son métabolisme hépatique par l'inducteur.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
l'inducteur et après son arrêt.
Risque d'hypothyroïdie clinique chez les patients hypothyroïdiens,
par augmentation du métabolisme de la T3 et de la T4.
+ IDÉLALISIB
Association DECONSEILLEEDiminution des concentrations plasmatiques d’idélalisib par
augmentation de son métabolisme hépatique par l'inducteur
enzymatique.
+ INHIBITEURS DE LA 5-ALPHA REDUCTASE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Diminution des concentrations plasmatiques de l’inhibiteur de la 5-
alpha réductase par l’inducteur enzymatique.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'inhibiteur de protéases par
augmentation de son métabolisme hépatique par l'inducteur.
+ INHIBITEURS DE TYROSINE KINASES MÉTABOLISÉS
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l’efficacité de
l’inhibiteur de tyrosine kinase, par augmentation de son
métabolisme par l’inducteur.
+ IVABRADINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’ivabradine
pendant l’association et après l’arrêt de l’inducteur.
Risque de diminution de l'efficacité de l’ivabradine, par
augmentation de son métabolisme par l’inducteur.
128
+ LÉDIPASVIR
CONTRE-INDICATIONDiminution importante des concentrations plasmatiques du
lédipasvir par augmentation de son métabolisme hépatique par
l'inducteur enzymatique.
+ LÉNACAPAVIR
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
+ METRONIDAZOLE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
métronidazole pendant le traitement par l’inducteur et après son arrêt.
Diminution des concentrations plasmatiques du métronidazole par
augmentation de son métabolisme hépatique par l’inducteur.
+ MIDAZOLAM
A prendre en compteRisque de diminution des concentrations plasmatiques du
midazolam par l'anticonvulsivant.
+ MINÉRALOCORTICOÏDES
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie des
corticoïdes pendant le traitement par l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité des
corticoïdes par augmentation de leur métabolisme hépatique par
l'inducteur : les conséquences sont particulièrement importantes
chez les addisoniens traités par l'hydrocortisone et en cas de
transplantation.
+ MONTELUKAST
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de l'anti-
asthmatique pendant le traitement par l'inducteur et après son arrêt.
Risque de baisse de l'efficacité du montélukast par augmentation
de son métabolisme hépatique par l'inducteur.
+ NIMODIPINE
Association DECONSEILLEE
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par l'inducteur et après
son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique par
l'inducteur.
+ OZANIMOD
Association DECONSEILLEEDiminution des concentrations des métabolites actifs de l’ozanimod
d’environ 60%.
+ PÉRAMPANEL
A prendre en compteDiminution importante (jusqu’aux deux-tiers) des concentrations de
pérampanel.
+ POSACONAZOLE
Précaution d'emploi
Surveillance clinique. Si possible, dosages plasmatiques du
posaconazole et adaptation éventuelle de sa posologie.
Diminution des concentrations plasmatiques et de l'efficacité du
posaconazole.
+ PRAZIQUANTEL
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques du
praziquantel, avec risque d'échec du traitement, par augmentation
de son métabolisme hépatique par l'inducteur.
+ PROCARBAZINE
A prendre en compteAugmentation des réactions d'hypersensibilité (hyperéosinophilie,
rash), par augmentation du métabolisme de la procarbazine par
l'inducteur.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et ECG. S'il y a lieu, adaptation de la posologie de
la propafénone pendant l'association et après l'arrêt de l'inducteur.
Diminution des concentrations plasmatiques de la propafénone par
augmentation de son métabolisme hépatique par l'inducteur.
+ QUETIAPINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
quétiapine par augmentation de son métabolisme hépatique par
l'inducteur, avec risque d’inefficacité.
129
+ QUININE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la quinine
pendant le traitement par l’inducteur et après son arrêt.
Risque de perte de l’efficacité de la quinine par augmentation de
son métabolisme hépatique par l’inducteur.
+ RANOLAZINE
Association DECONSEILLEERisque de diminution importante des concentrations de ranolazine.
+ RIVAROXABAN
Association DECONSEILLEEDiminution des concentrations plasmatiques de rivaroxaban, avec
risque de diminution de l'effet thérapeutique.
+ SACITUZUMAB
A prendre en comptePour le SN38 lié au sacizutumab (govitécan) : risque de diminution
de son exposition, par augmentation de son métabolisme.
+ SOTORASIB
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du sotorasib,
avec risque de moindre efficacité.
+ STIRIPENTOL
Précaution d'emploi
Surveillance clinique et dosage plasmatique, lorsque cela est possible,
de l'inducteur associé au stiripentol et adaptation éventuelle de sa
posologie.
Augmentation des concentrations plasmatiques de l'inducteur, avec
risque de surdosage, par inhibition de son métabolisme hépatique
par le stiripentol.
+ TELITHROMYCINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de la télithromycine,
avec risque d'échec du traitement anti-infectieux, par augmentation
de son métabolisme hépatique par l'inducteur.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et, si besoin, de la théophyllinémie. Adaptation
éventuelle de la posologie de la théophylline pendant le traitement par
l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
théophylline par augmentation de son métabolisme hépatique par
l'inducteur.
+ TIAGABINE
Précaution d'emploi
Une augmentation de la posologie de tiagabine peut s'avérer
nécessaire en cas d'association à un anticonvulsivant inducteur
enzymatique.
Diminution des concentrations plasmatiques de la tiagabine par
augmentation de son métabolisme hépatique par l'inducteur.
+ TICAGRELOR
Association DECONSEILLEEDiminution importante des concentrations plasmatiques de
ticagrelor par augmentation de son métabolisme hépatique par
l'inducteur enzymatique, avec risque de diminution de l’effet
thérapeutique.
+ ULIPRISTAL
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par l’inducteur.
+ VELPATASVIR
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par
l’inducteur, avec possible retentissement sur l’efficacité.
+ VITAMINE D
Précaution d'emploi
Dosage des concentrations de vitamine D et supplémentation si
nécessaire.
Diminution des concentrations de vitamine D plus marquée qu’en
l’absence d'inducteur.
130
+ VORICONAZOLE
CI - ASDEC
Contre-indication :
- pour carbamazépine, phénobarbital, primidone
Association déconseillée :
- pour apalutamide, enzalutamide
- pour phénytoïne, fosphénytoïne
Si l'association ne peut être évitée, surveillance clinique étroite, dosage
des concentrations plasmatiques de phénytoïne et adaptation
éventuelle des posologies pendant l'association et après l'arrêt du
voriconazole.
- pour carbamazépine, phénobarbital, primidone : Risque de baisse
de l'efficacité du voriconazole par augmentation de son
métabolisme hépatique par l'inducteur.
- pour phénytoïne, fosphénytoïne :
Diminution importante des concentrations plasmatiques du
voriconazole avec risque de perte d'efficacité, par augmentation de
son métabolisme hépatique par la phénytoïne, d'une part, et
augmentation des concentrations plasmatiques de la phénytoïne
par diminution de son métabolisme hépatique par le voriconazole,
d'autre part.
+ VOXELOTOR
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du voxelotor,
avec risque de moindre efficacité.
INHIBITEURS DE LA 5-ALPHA REDUCTASE
(dutasteride, finasteride)
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Diminution des concentrations plasmatiques de l’inhibiteur de la 5-
alpha réductase par l’inducteur enzymatique.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de l’inhibiteur de la 5-
alpha réductase par le millepertuis.
+ RIFAMPICINE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Diminution des concentrations plasmatiques de l’inhibiteur de la 5-
alpha réductase par l’inducteur enzymatique.
INHIBITEURS DE LA CATÉCHOL-O-MÉTHYLTRANSFÉRASE (COMT)
(entacapone, tolcapone)
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONPotentialisation des effets pharmacologiques, et notamment
vasopresseurs, des catécholamines par inhibition conjuguée de
leur métabolisme.
INHIBITEURS DE LA PHOSPHODIESTERASE DE TYPE 5
(avanafil, sildenafil, tadalafil, vardenafil)
+ ALPHABLOQUANTS À VISÉE UROLOGIQUE
ASDEC - PE
Association déconseillée :
- avec la doxazosine
Précaution d'emploi :
- avec les autres alpha-bloquants
Débuter le traitement aux posologies minimales recommandées et
adapter progressivement les doses si besoin.
Risque d’hypotension orthostatique, notamment chez le sujet âgé.
+ ANTIHYPERTENSEURS ALPHA-BLOQUANTS
ASDEC - PE
Association déconseillée :
- avec la doxazosine
Précaution d'emploi :
- avec les autres alpha-bloquants
Débuter le traitement aux posologies minimales recommandées et
adapter progressivement les doses si besoin.
Risque d’hypotension orthostatique, notamment chez le sujet âgé.
+ DÉRIVÉS NITRÉS ET APPARENTÉS
CONTRE-INDICATIONRisque d'hypotension importante (effet synergique) pouvant
aggraver l'état d'ischémie myocardique et provoquer notamment un
accident coronarien aigu.
+ INHIBITEURS PUISSANTS DU CYP3A4
CI - ASDEC - PE
Pour connaître les risques et les niveaux de contrainte de chaque
IPDE5 avec les inhibiteurs puissants du CYP3A4, il convient de se
reporter aux AMM specifiques à chacun d'eux.
Augmentation (très importante pour l'avanafil et le vardénafil) des
concentrations plasmatiques de l'IPDE5, avec risque d'hypotension
(sévère avec le vardénafil).
131
+ RIOCIGUAT
CONTRE-INDICATIONRisque d'hypotension importante (effet synergique).
INHIBITEURS DE LA XANTHINE OXYDASE
(allopurinol, febuxostat)
+ ANTIPURINES
CONTRE-INDICATIONInsuffisance médullaire éventuellement grave.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et contrôle de la théophyllinémie jusqu'à deux à
trois semaines après la mise en route du traitement par l'inhibiteur ; s'il y
a lieu, adaptation de la posologie pendant le traitement par l'association.
En cas de posologies élevées de l'inhibiteur, augmentation des
concentrations plasmatiques de théophylline par inhibition de son
métabolisme.
INHIBITEURS DE L'ENZYME DE CONVERSION
(benazepril, captopril, cilazapril, enalapril, fosinopril, lisinopril, moexipril, périndopril, quinapril, ramipril, trandolapril, zofenopril)
+ ACIDE ACETYLSALICYLIQUE
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Pour des doses anti-inflammatoires d'acide acétylsalicylique (>= 1g
par prise et/ou >= 3g par jour) ou pour des doses antalgiques ou
antipyrétiques (>= 500 mg par prise et/ou < 3g par jour) :
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Par ailleurs, réduction de
l'effet antihypertenseur.
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
A prendre en compteDans les indications où cette association est possible, risque accru
de dégradation de la fonction rénale, voire insuffisance rénale
aiguë, et majoration de l'hyperkaliémie, ainsi que de l'hypotension
et des syncopes.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Précaution d'emploi
Hydrater le malade et surveiller la fonction rénale en début de traitement
et régulièrement pendant l’association.
Insuffisance rénale aiguë chez le patient à risque (âgé, déshydraté,
sous diurétiques, avec une fonction rénale altérée), par diminution
de la filtration glomérulaire secondaire à une diminution de la
synthèse des prostaglandines rénales. Ces effets sont
généralement réversibles. Par ailleurs, réduction de l’effet
antihypertenseur.
+ DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
ASDEC - PE
Association déconseillée :
- si l'association est justifiée, contrôle strict de la kaliémie et de la
fonction rénale.
Précaution d'emploi :
- pour la spironolactone à des doses comprises entre 12,5 mg et 50
mg/jour, et pour l’éplérénone utilisées dans le traitement de
l'insuffisance cardiaque, ainsi qu'en cas d'hypokaliémie : contrôle strict
de la kaliémie et de la fonction rénale.
Risque d'hyperkaliémie (potentiellement létale) surtout en cas
d'insuffisance rénale (addition des effets hyperkaliémiants).
+ DIURÉTIQUES HYPOKALIÉMIANTS
Précaution d'emploi
Dans l'hypertension artérielle, lorsqu'un traitement diurétique préalable
a pu entraîner une déplétion hydrosodée, il faut :
- soit arrêter le diurétique avant de débuter le traitement par l'IEC, et
réintroduire un diurétique hypokaliémiant si nécessaire ultérieurement ;
- soit administrer des doses initiales réduites d'IEC et augmenter
progressivement la posologie.
Dans l'insuffisance cardiaque congestive traitée par diurétiques,
commencer par une dose très faible d'IEC, éventuellement après
réduction de la dose du diurétique hypokaliémient associé.
Dans tous les cas : surveiller la fonction rénale (créatininémie) dans les
premières semaines du traitement par l'IEC.
Risque d'hypotension artérielle brutale et/ou d'insuffisance rénale
aiguë lors de l'instauration ou de l'augmentation de la posologie
d'un traitement par un inhibiteur de l'enzyme de conversion en cas
de déplétion hydrosodée préexistante.
+ EPLERENONE
Précaution d'emploi
Contrôle strict de la kaliémie et de la fonction rénale pendant
l’association.
Majoration du risque d’hyperkaliémie, notamment chez le sujet âgé.
+ ESTRAMUSTINE
Association DECONSEILLEERisque de majoration des effets indésirables à type d'oedème
angio-neurotique (angio-oedème).
132
+ GLIPTINES
A prendre en compteRisque de majoration de la survenue d'un angio-œdème d'origine
bradykinique pouvant être fatal.
+ INSULINE
Précaution d'emploi
Renforcer l'autosurveillance glycémique.
L'utilisation des IEC peut entraîner une majoration de l'effet
hypoglycémiant chez le diabétique traité par insuline. La survenue
de malaises hypoglycémiques semble exceptionnelle (amélioration
de la tolérance au glucose qui aurait pour conséquence une
réduction des besoins en insuline).
+ LITHIUM
Association DECONSEILLEE
Si l'usage d'un IEC est indispensable, surveillance stricte de la lithémie
et adaptation de la posologie du lithium.
Augmentation de la lithémie pouvant atteindre des valeurs toxiques
(diminution de l'excrétion rénale du lithium).
+ OR
A prendre en compteAvec les sels d'or administrés par voie IV : risque de réaction
«nitritoïde» à l’introduction de l’IEC (nausées, vomissements, effets
vasomoteurs à type de flush, hypotension, éventuellement
collapsus).
+ POTASSIUM
Association DECONSEILLEE
Sauf s'il existe une hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (
addition des effets hyperkaliémiants).
+ SACUBITRIL
CONTRE-INDICATIONAugmentation du risque d'angioedème.
+ SIROLIMUS
A prendre en compteMajoration du risque d’angio-oedème.
+ SPIRONOLACTONE
Précaution d'emploi
Vérifier au préalable l’absence d’hyperkaliémie et d’insuffisance rénale.
Surveillance biologique étroite de la kaliémie et de la créatininémie (1
fois par semaine pendant le premier mois, puis une fois par mois
ensuite).
Avec la spironolactone à la posologie de 12,5 à 50 mg par jour, et
avec des doses faibles d’IEC.
Dans le traitement de l’insuffisance cardiaque de classe III ou IV
(NYHA) avec fraction d’éjection <35 % et préalablement traitée par
l’association inhibiteur de conversion + diurétique de l’anse : risque
d’hyperkaliémie, potentiellement létale, en cas de non-respect des
conditions de prescription de cette association.
+ SULFAMIDES HYPOGLYCÉMIANTS
Précaution d'emploi
Renforcer l'autosurveillance glycémique.
L'utilisation des IEC peut entraîner une majoration de l'effet
hypoglycémiant chez le diabétique traité par sulfamides
hypoglycémiants. La survenue de malaises hypoglycémiques
semble exceptionnelle (amélioration de la tolérance au glucose qui
aurait pour conséquence une réduction des besoins en sulfamides
hypoglycémiants).
+ TEMSIROLIMUS
A prendre en compteMajoration du risque d’angio-oedème.
INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
(atorvastatine, fluvastatine, pitavastatine, pravastatine, rosuvastatine, simvastatine)
+ ACIDE FUSIDIQUE
CONTRE-INDICATION
Arrêter le traitement par l'inhibiteur de l'HMG Co-A
réductase avant d'initier un traitement par acide fusidique ou utiliser un
autre antibiotique.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ COBIMÉTINIB
A prendre en compteRisque majoré de rhabdomyolyse.
133
+ COLCHICINE
Précaution d'emploi
Surveillance clinique et biologique, notamment au début de l'association.
Risque de majoration des effets indésirables musculaires de ces
substances, et notamment de rhabdomyolyse.
+ DAPTOMYCINE
Association DECONSEILLEE
Si l’association ne peut être évitée, renforcer la surveillance biologique
(dosage des CPK plus d’une fois par semaine) et surveillance clinique
étroite.
Risque d’addition des effets indésirables (dose-dépendant) à type
de rhabdomyolyse.
+ ELTROMBOPAG
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
statine.
Risque de majoration de la toxicité des statines, par inhibition de
leur recapture hépatique.
+ FIBRATES
CI - ASDEC
L'association d'un fibrate et d'une statine est au minmum déconseillée.
Avec la simvastatine, ne pas dépasser 10 mg ( cette restriction de
doses ne concerne pas le fénofibrate).
La contre-indication s'applique :
- entre le gemfibrozil et la simvastatine
- pour des doses de rosuvastatine de 40 mg
Risque d'addition d'effets indésirables (dose-dépendants) à type de
rhabdomyolyse. En outre, avec le gemfibrozil, diminution du
métabolisme de la simvastatine et de la rosuvastatine, ce qui
majore le risque musculaire, ainsi que la néphrotoxicité de la
rosuvastatine.
+ GLIPTINES
Précaution d'emploi
Le contrôle régulier de la fonction rénale et le strict respect des doses
sont impératifs.
Possibilité de survenue d’effets indésirables musculaires à
l’introduction d’une gliptine, malgré le traitement antérieur par
statine bien toléré.
+ GRAZOPREVIR + ELBASVIR
Précaution d'emploi
Surveillance clinique et biologique pendant l’association. La dose de
statine ne doit pas dépasser 20 mg par jour (10 mg avec la
rosuvastatine).
Augmentation des concentrations plasmatiques de
l’hypochlestérolémiant par augmentation de son absorption
intestinale.
+ LÉDIPASVIR
CI - PE
Contre-indication :
- avec la rosuvastatine.
Précaution d'emploi :
- avec les autres inhibiteurs de l'HMG Co-A réductase.
Surveillance clinique et biologique. Adaptation éventuelle de la
posologie de la statine.
Risque d’augmentation des concentrations plasmatiques de la
statine et de ses effets indésirables à type de rhabdomyolyse.
+ LENALIDOMIDE
Précaution d'emploi
Renforcer le contrôle clinique et biologique, notamment durant les
premières semaines de traitement.
Risque majoré de survenue de rhabdomyolyses.
+ LÉTERMOVIR
ASDEC - PE
Association déconseillée:
- avec simvastatine, pitavastatine, rosuvastatine
Précaution d'emploi (en cas d’utilisation du létermovir seul):
- ne pas dépasser 20 mg/ jour d’atorvastatine
- adaptation éventuelle de la posologie de fluvastatine et de
pravastatine,
Risque d’augmentation des concentrations plasmatiques de la
statine et de ses effets indésirables à type de rhabdomyolyse.
+ ROXADUSTAT
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la statine pendant
le traitement par roxadustat.
Augmentation d’un facteur 2 à 3 de l’exposition de la statine, par
diminution de son métabolisme par le roxadustat.
134
INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Le ritonavir est désormais utilisé à la dose de 100 mg 2 fois par jour en association à un autre inhibiteur de protéase, dans le but d'augmenter de façon très
significative la biodisponibilité de l'inhibiteur de protéase associé (ou boosté), ce qui permet d'augmenter ainsi l'efficacité du traitement antirétroviral. Eu égard à ce
schéma thérapeutique, chaque inhibiteur de protéase acquiert de la sorte les propriétés d'inhibition puissante du CYP3A4 que possède le ritonavir, et ce, même
lorsque celui-ci est donné à doses 6 fois moindres que lors des premières années de son utilisation. En pratique, ceci revient donc à considérer tous les inhibiteurs de
protéase comme des inhibiteurs enzymatiques de puissance comparable. Par conséquent, les interactions communes à cette classe découlent, pour la plupart, de
cette propriété.
(atazanavir, darunavir, fosamprenavir, lopinavir, nirmatrelvir, ritonavir, saquinavir, tipranavir)
+ AFATINIB
Précaution d'emploi
Il est recommandé d’administrer l'inhibiteur de protéases le plus à
distance possible de l’afatinib, en respectant de préférence un
intervalle de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatiques d’afatinib par
augmentation de son absorption par l'inhibiteur de protéases.
+ ALBENDAZOLE
Précaution d'emploi
Surveillance clinique de la réponse thérapeutique et adaptation
éventuelle de la posologie de l’albendazole pendant le traitement avec
l’inducteur enzymatique et après son arrêt.
Diminution importante des concentrations plasmatiques de
l’albendazole et de son métabolite actif par le ritonavir, avec risque
de baisse de son efficacité.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant la durée du traitement.
Variation de l'effet de l'antivitamine K, le plus souvent dans le sens
d'une diminution.
+ ATORVASTATINE
Association DECONSEILLEE
Utiliser des doses plus faibles d'atorvastatine. Si l'objectif thérapeutique
n'est pas atteint, utiliser une autre statine non concernée par ce type
d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l'atorvastatine).
+ ATOVAQUONE
Association DECONSEILLEEDiminution, éventuellement très importante, des concentrations
plasmatiques de l’atovaquone par augmentation de son
métabolisme.
+ BUPRENORPHINE
A prendre en compteRisque de majoration ou de diminution des effets de la
buprénorphine, à la fois par inhibition et accélération de son
métabolisme par l’inhibiteur de protéases.
+ CLARITHROMYCINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Augmentation des concentrations de la clarithromycine et de son
métabolite actif par diminution de son métabolisme hépatique par
l'inhibiteur de protéases.
+ CYPROTERONE
ASDEC - PE
Association déconseillée
- dans son utilisation comme contraceptif hormonal: utiliser de
préférence une autre méthode de contraception en particulier de type
mécanique, pendant la durée de l'association et un cycle suivant.
Précaution d'emploi
- dans ses indications comme anti-androgène: surveillance clinique et
adaptation éventuelle de la posologie de la cyprotérone pendant
l'association et après son arrêt.
Risque de diminution de l'efficacité de la cyprotérone.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et, s’il y a lieu, de l’ECG et de la digoxinémie, avec
adaptation éventuelle de la posologie de digoxine.
Augmentation de la digoxinémie, plus marquée pour la voie
intraveineuse, par augmentation de l’absorption de la digoxine ou
diminution de sa clairance rénale.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du ritonavir.
Risque de diminution de l'efficacité contraceptive par diminution
des concentrations en contraceptif hormonal, dûe à l'augmentation
de son métabolisme hépatique par le ritonavir.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique et adaptation éventuelle de la
posologie des hormones thyroïdiennes.
Risque de baisse de l’efficacité des hormones thyroïdiennes par
augmentation de leur métabolisme hépatique par le ritonavir.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation de sa
posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
135
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'inhibiteur de protéases par
augmentation de son métabolisme hépatique par l'inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en compte
Pour connaître les risques et les niveaux de contrainte de chaque
inhibiteur de protéase boosté par le ritonavir avec les inhibiteurs
puissants du CYP3A4, il convient de se reporter aux AMM spécifiques à
chacun d'eux.
Risque d’augmentation des concentrations plasmatiques de
l’inhibiteur de protéase boosté par le ritonavir ou de l’inhibiteur du
CYP3A4.
+ ITRACONAZOLE
Précaution d'emploi
Surveillance clinique lors de l’association. L’administration de doses
élevées d’itraconazole (>200 mg par jour) n’est pas recommandée.
Risque d’augmentation des concentrations d’itraconazole par
l’inhibiteur de protéases.
+ LAMOTRIGINE
ASDEC - PE
Association déconseillée
- Eviter de mettre en route le traitement par ritonavir pendant la période
d’ajustement posologique de la lamotrigine.
Précaution d'emploi
- Surveillance clinique et adaptation de la posologie de la lamotrigine
lors de la mise en route du traitement par ritonavir.
Risque de diminution des concentrations et de l’efficacité de la
lamotrigine par augmentation de son métabolisme hépatique par le
ritonavir.
+ METHADONE
Précaution d'emploi
Surveillance clinique régulière et adaptation éventuelle de la posologie
de méthadone.
Diminution des concentrations plasmatiques de méthadone avec
risque d'apparition d'un syndrome de sevrage par augmentation de
son métabolisme hépatique par le ritonavir.
+ MILLEPERTUIS
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler les concentrations plasmatiques (ou
l'efficacité) de l'inhibiteur de protéases avant puis après l'arrêt du
millepertuis.
Diminution des concentrations plasmatiques de l'inhibiteur de
protéases, en raison de l'effet inducteur enzymatique du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet dont les conséquences peuvent être éventuellement graves
(baisse de l'efficacité antirétrovirale).
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'inhibiteur de protéases
boosté par ritonavir.
+ PROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique (préservatif ou stérilet), pendant la durée de
l'association et un cycle suivant.
Risque de diminution de l'efficacité contraceptive par diminution
des concentrations en contraceptif hormonal, dûe à l'augmentation
de son métabolisme hépatique par le ritonavir.
+ QUINIDINE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ RIFABUTINE
Précaution d'emploi
Réduction de la dose de rifabutine (150 mg 1 jour sur deux).
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'inhibiteur de protéases (ce
d'autant que la posologie de la rifabutine est élevée) d'une part, et
risque d'augmentation des effets indésirables (uvéites) de la
rifabutine, d'autre part.
+ RIFAMPICINE
CONTRE-INDICATION
Dans l'attente de données complémentaires avec les inhibiteurs de
protéases "boostés".
Diminution très importante des concentrations plasmatiques de
l'inhibiteur de protéases, par augmentation de son métabolisme
hépatique par la rifampicine.
Pour l'association (saquinavir + ritonavir) :
risque de toxicité hépatocellulaire sévère.
+ ROSUVASTATINE
Précaution d'emploi
Surveillance clinique et biologique.
Augmentation des concentrations plasmatiques de la rosuvastatine
par augmentation de son absorption.
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
136
+ TÉNOFOVIR ALAFÉNAMIDE
Précaution d'emploi
En cas de co-administration, la dose de ténofovir alafénamide doit être
limitée à 10 mg par jour. L’association avec les autres inhibiteurs de
protéases du VIH n’a pas été étudiée.
Avec l'atazanavir, le darunavir ou le lopinavir, augmentation des
concentrations plasmatiques du ténofovir alafénamide par
augmentation de son absorption.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par l'inhibiteur de protéases et après son arrêt.
Diminution des concentrations plasmatiques de la théophylline, par
augmentation de son métabolisme hépatique.
+ ULIPRISTAL
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par le ritonavir.
+ VENLAFAXINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ VORICONAZOLE
Association DECONSEILLEEBaisse très importante des concentrations de l’antifongique par
augmentation de son métabolisme par le ritonavir, avec risque
d’échec du traitement.
INHIBITEURS DE TYROSINE KINASES MÉTABOLISÉS
(abémaciclib, acalabrutinib, axitinib, bosutinib, brigatinib, cabozantinib, céritinib, cobimétinib, crizotinib, dabrafénib, dasatinib, entrectinib, erlotinib, fédratinib,
fostamatinib, gefitinib, giltéritinib, ibrutinib, imatinib, lapatinib, larotrectinib, lorlatinib, nilotinib, osimertinib, palbociclib, pazopanib, pémigatinib, ponatinib, pralsétinib,
ribociclib, riprétinib, ruxolitinib, selpercatinib, sélumétinib, sorafenib, sunitinib, tucatinib, upadacitinib, vandétanib, zanubrutinib)
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compte
- sauf avec l'entrectinib et le vandétanib.
Risque de diminution de la biodisponibilité de l’inhibiteur de tyrosine
kinases, en raison de son absorption pH-dépendante.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compte
- sauf avec l'entrectinib, le fédratinib, l'imatinib, le tucatinib et le
vandétanib
Risque de diminution de la biodisponibilité de l’inhibiteur de tyrosine
kinases, en raison de son absorption pH-dépendante.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l’efficacité de
l’inhibiteur de tyrosine kinase, par augmentation de son
métabolisme par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
ASDEC - PE
Association déconseillée :
- avec l'axitinib, le bosutinib, le cabozantinib, le céritinib, le cobimétinib,
le dabrafenib, le dasatinib, l'entrectinib, le nilotinib, le sunitinib.
- avec l'ibrutinib et le ribociclib: si l’association ne peut être évitée,
surveillance clinique étroite et réduction de la dose pendant la durée de
l’association voire interruption temporaire ou définitive.
Précaution d'emploi avec les autres ITK (sauf abrocitinib, osimertinib,
tucatinib et vandétanib):
Surveillance clinique.
Risque de majoration des effets indésirables de l’inhibiteur de
tyrosine kinase par diminution de son métabolisme.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques et de l’efficacité de
l’inhibiteur de tyrosine kinase, par augmentation de son
métabolisme par le millepertuis.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l’efficacité de
l’inhibiteur de tyrosine kinase, par augmentation de son
métabolisme par l’inducteur.
INHIBITEURS D'INTÉGRASE
(bictégravir, cabotegravir, dolutégravir, raltégravir)
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium à distance de l’antirétroviral (plus de 2
heures, si possible).
Diminution de l'absorption digestive des inhibiteurs d’intégrase.
137
+ FER
Précaution d'emploi
Prendre les sels de fer à distance de l’antirétroviral (plus de 2 heures, si
possible).
Diminution de l'absorption digestive des inhibiteurs d’intégrase.
+ MAGNÉSIUM
Précaution d'emploi
Prendre les sels de magnésium à distance de l’antirétroviral (plus de 2
heures, si possible).
Diminution de l'absorption digestive des inhibiteurs d’intégrase.
+ ZINC
Précaution d'emploi
Prendre les sels de zinc à distance de l’antirétroviral (plus de 2 heures,
si possible).
Risque de diminution de l'absorption digestive des inhibiteurs
d’intégrase, par chélation par le cation divalent.
INHIBITEURS DIRECTS DE LA THROMBINE À INDICATION SPÉCIFIQUE
(argatroban, bivalirudine)
+ AUTRES MÉDICAMENTS AGISSANT SUR L'HÉMOSTASE
A prendre en compteMajoration du risque hémorragique.
INHIBITEURS PUISSANTS DU CYP3A4
Certains médicaments possèdent la capacité d’inhiber fortement le CYP3A4, une enzyme qui intervient dans le métabolisme de nombreux médicaments. Lorsque
l’activité de cette enzyme est inhibée, elle n’est plus en mesure de métaboliser le médicament qui va alors s’accumuler. Si la marge thérapeutique de ce médicament
est étroite et qu’il n'y a pas d’autre voie métabolique efficace, le risque d’observer une interaction cliniquement significative devient élevé.
Les principaux inhibiteurs du CYP3A4 sont :
- les azolés antifongiques (kétoconazole, itraconazole, voriconazole, posaconazole),
- les inhibiteurs de protéase, représentés ici par le ritonavir, avec lequel ils sont boostés,
- certains macrolides (la clarithromycine, l’érythromycine, la télithromycine).
Parmi les substrats du CYP3A4 à marge thérapeutique étroite et pour lesquels un risque de surdosage est plus particulièrement à redouter en cas d’association avec
un inhibiteur du CYP3A4, on peut citer :
- l'ergotamine, alcaloïde vasocontricteur de l'ergot de seigle : risque de nécrose des extrémités ;
- les immunosuppresseurs (ciclosporine, tacrolimus…) : risque néphrotoxique ;
- certaines statines (simvastatine, et dans une moindre mesure, atorvastatine) : risque musculaire, notamment rhabdomyolyse ;
- certains médicaments donnant des torsades de pointes : pimozide, halofantrine, luméfantrine ;
- des médicaments dépresseurs du centre respiratoire : alfentanil, sufentanil, oxycodone, midazolam ;
- certains cytotoxiques : bortezomib, docétaxel, inhibiteurs des tyrosine kinases.
Pour connaître les risques et les niveaux de contrainte de chacun de ces substrats, il convient de se reporter aux interactions spécifiques avec chaque inhibiteur.
(clarithromycine, cobicistat, erythromycine, itraconazole, ketoconazole, posaconazole, ritonavir, telithromycine, tucatinib, voriconazole)
+ ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
CONTRE-INDICATIONRisque de vasoconstriction coronaire ou des extrémités
(ergotisme), ou de poussées hypertensives.
+ ALFENTANIL
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’analgésique
opiacé en cas de traitement par un inhibiteur puissant du CYP3A4.
Augmentation de l'effet dépresseur respiratoire de l'analgésique
opiacé par diminution de son métabolisme hépatique.
+ ALFUZOSINE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de
l’alfuzosine et de ses effets indésirables.
+ ALPRAZOLAM
A prendre en comptePossible augmentation de l'effet sédatif de l'alprazolam.
+ ANTAGONISTES DES CANAUX CALCIQUES
ASDEC - PE
Association déconseillée:
- avec la lercanidipine.
Précaution d'emploi:
- avec les autres antagonistes des canaux calciques.
Surveillance clinique et adaptation posologique pendant le traitement
par l’inhibiteur enzymatique et après son arrêt.
Majoration des effets indésirables de l’antagoniste des canaux
calciques, le plus souvent à type d'hypotension et d'oedèmes,
notamment chez le sujet âgé.
138
+ ANTISPASMODIQUES URINAIRES
CI - ASDEC - PE
Contre-indication :
- avec la darifénacine
- avec la fésotérodine et la solifénacine, en cas d'insuffisance rénale ou
hépatique, modérée à sévère.
Association déconseillée :
- avec la toltérodine
Précaution d'emploi:
- avec la fésotérodine ou la solifénacine, chez le patient à fonction
rénale et hépatique normales, réduire la dose à 4 mg ou 5 mg,
respectivement, en cas d'association à un inhibiteur puissant du
CYP3A4.
A prendre en compte :
- avec l'oxybutynine.
Risque de majoration des effets indésirables.
+ APIXABAN
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l’apixaban par
l'inhibiteur, avec majoration du risque de saignement.
+ BÉDAQUILINE
Association DECONSEILLEE
Si l’association est nécessaire, une surveillance ECG plus fréquente et
une surveillance des transaminases sont recommandées.
Augmentation des concentrations plasmatiques de bédaquiline par
diminution de son métabolisme hépatique par l’inhibiteur.
+ BORTEZOMIB
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
bortezomib pendant la durée du traitement par l’inhibiteur enzymatique.
Risque de majoration des effets indésirables, notamment
neurologiques, du bortezomib par diminution de son métabolisme.
+ BOSENTAN
Précaution d'emploi
Surveillance clinique et biologique pendant l’association.
Risque majoré des effets indésirables du bosentan, notamment
d’atteintes hépatiques, par diminution de son métabolisme par
l'inhibiteur.
+ BRENTUXIMAB
A prendre en compteAugmentation des concentrations du métabolite actif du
brentuximab, avec risque de neutropénie.
+ CABAZITAXEL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
cabazitaxel pendant le traitement par l’inhibiteur enzymatique.
Risque de majoration des effets indésirables dose-dépendants du
cabazitaxel par inhibition de son métabolisme par l’inhibiteur
enzymatique.
+ COBICISTAT
A prendre en compte
Pour connaître les risques et les niveaux de contrainte de chaque
interaction, il convient de se reporter aux AMM specifiques à chaque
spécialité.
Risque d’augmentation des concentrations plasmatiques du
cobicistat ou de l’inhibiteur du CYP3A4.
+ COLCHICINE
CI - ASDEC
Contre-indication :
- avec les macrolides
Association déconseillée :
- avec les antifongiques azolés, les inhibiteurs de protéases boostés par
ritonavir et le cobicistat
Augmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
+ CORTICOÏDES MÉTABOLISÉS, NOTAMMENT INHALÉS
Association DECONSEILLEE
Préférer un corticoïde non métabolisé.
En cas d’utilisation prolongée par voie orale ou inhalée :
augmentation des concentrations plasmatiques du corticoïde par
diminution de son métabolisme hépatique par l’inhibiteur, avec
risque d’apparition d’un syndrome cushingoïde
voire d’une insuffisance surrénalienne.
+ DAPOXÉTINE
CONTRE-INDICATIONRisque de majoration des effets indésirables, notamment à type de
vertiges ou de syncopes.
+ DÉLAMANID
Association DECONSEILLEE
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
139
+ DISOPYRAMIDE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
disopyramide.
Risque d’augmentation des effets indésirables du disopyramide par
diminution de son métabolisme.
+ DOCETAXEL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
docétaxel pendant le traitement par l’inhibiteur enzymatique.
Risque de majoration des effets indésirables dose-dépendants du
docétaxel par inhibition de son métabolisme par l’inhibiteur
enzymatique.
+ DOMPERIDONE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de dompéridone
par diminution de son métabolisme hépatique par l’inhibiteur.
+ DRONEDARONE
CONTRE-INDICATIONAugmentation importante des concentrations de dronédarone par
diminution de son métabolisme.
+ ÉLIGLUSTAT
CONTRE-INDICATIONChez les patients ayant un génotype de métaboliseurs lents du
CYP2D6, risque de majoration des effets indésirables de l’éliglustat.
+ EPLERENONE
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques de
l’éplérénone par l'inhibiteur et de ses effets indésirables,
notamment l’hyperkaliémie.
+ ESZOPICLONE
CI - PE
Contre-indication
- chez les patients âgés
Précaution d'emploi
En cas d’association chez les sujets non âgés, une réduction de la dose
d’eszopiclone peut être nécessaire.
Augmentation de l'effet sédatif de l’eszopiclone.
+ FENTANYL
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
l’analgésique opiacé en cas de traitement par un inhibiteur puissant du
CYP3A4.
Risque d'augmentation de l’effet dépresseur respiratoire de
l’analgésique opiacé par légère diminution de son métabolisme
hépatique.
+ GLASDÉGIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Risque de majoration des effets indésirables du glasdégib par
diminution de son métabolisme.
+ GRAZOPREVIR + ELBASVIR
CI - ASDEC
Contre-indication
- avec le ritonavir et le cobicistat
Association déconseillée
- avec les autres inhibiteurs du CYP3A4
Augmentation des concentrations plasmatiques de grazoprévir et
d’elbasvir.
+ HALOFANTRINE
Association DECONSEILLEE
Si cela est possible, interrompre l'inhibiteur. Si l'association ne peut être
évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
+ IDÉLALISIB
A prendre en compteAugmentation des concentrations plasmatiques d’idélalisib par
diminution de son métabolisme hépatique par l’inhibiteur.
+ INHIBITEURS DE LA PHOSPHODIESTERASE DE TYPE 5
CI - ASDEC - PE
Pour connaître les risques et les niveaux de contrainte de chaque
IPDE5 avec les inhibiteurs puissants du CYP3A4, il convient de se
reporter aux AMM specifiques à chacun d'eux.
Augmentation (très importante pour l'avanafil et le vardénafil) des
concentrations plasmatiques de l'IPDE5, avec risque d'hypotension
(sévère avec le vardénafil).
140
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
A prendre en compte
Pour connaître les risques et les niveaux de contrainte de chaque
inhibiteur de protéase boosté par le ritonavir avec les inhibiteurs
puissants du CYP3A4, il convient de se reporter aux AMM spécifiques à
chacun d'eux.
Risque d’augmentation des concentrations plasmatiques de
l’inhibiteur de protéase boosté par le ritonavir ou de l’inhibiteur du
CYP3A4.
+ INHIBITEURS DE TYROSINE KINASES MÉTABOLISÉS
ASDEC - PE
Association déconseillée :
- avec l'axitinib, le bosutinib, le cabozantinib, le céritinib, le cobimétinib,
le dabrafenib, le dasatinib, l'entrectinib, le nilotinib, le sunitinib.
- avec l'ibrutinib et le ribociclib: si l’association ne peut être évitée,
surveillance clinique étroite et réduction de la dose pendant la durée de
l’association voire interruption temporaire ou définitive.
Précaution d'emploi avec les autres ITK (sauf abrocitinib, osimertinib,
tucatinib et vandétanib):
Surveillance clinique.
Risque de majoration des effets indésirables de l’inhibiteur de
tyrosine kinase par diminution de son métabolisme.
+ IRINOTECAN
Association DECONSEILLEERisque de majoration des effets indésirables de l’irinotécan par
augmentation des concentrations plasmatiques de son métabolite
actif.
+ ISAVUCONAZOLE
CI - PE
Contre-indication:
- avec le kétoconazole
Précaution d'emploi:
- avec les autres inhibiteurs puissants du CYP3A4
Augmentation des concentrations plasmatiques d’isavuconazole
par diminution de son métabolisme hépatique par l’inhibiteur.
+ IVABRADINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l’ivabradine et
par conséquent de ses effets indésirables (inhibition de son
métabolisme hépatique par l’inhibiteur).
+ IVACAFTOR (SEUL OU ASSOCIÉ)
Précaution d'emploi
Se référer à l'AMM pour les adaptations posologiques.
Augmentation des concentrations d’ivacaftor, avec risque de
majoration des effets indésirables.
+ LOMITAPIDE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du lomitapide par
diminution de son métabolisme hépatique par l’inhibiteur.
+ LUMEFANTRINE
Association DECONSEILLEE
Si cela est possible, interrompre l’inhibiteur. Si l’association ne peut être
évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ LURASIDONE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la lurasidone
par diminution de son métabolisme hépatique par l’inhibiteur.
+ MARAVIROC
Précaution d'emploi
La dose de maraviroc doit être diminuée à 150 mg deux fois par jour en
cas de co-administration avec cet inhibiteur.
A l'exception du tipranavir boosté par ritonavir où la dose de maraviroc
doit être de 300 mg deux fois par jour.
Augmentation des concentrations de maraviroc par l’inhibiteur.
+ MIDAZOLAM
ASDEC - PE
Association déconseillée:
- avec le midazolam per os
Précaution d'emploi avec :
- avec le midazolam IV et sublingual
Surveillance clinique et réduction de la posologie de midazolam en cas
de traitement par l'inhibiteur.
Augmentation des concentrations plasmatiques de midazolam par
diminution de son métabolisme hépatique, avec majoration de la
sédation.
+ MIDOSTAURINE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Augmentation des effets indésirables de la midostaurine par
l’inhibiteur.
141
+ NALOXEGOL
CONTRE-INDICATIONAugmentation très importante des concentrations du naloxegol par
l’inhibiteur.
+ OLAPARIB
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 150 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par
l’inhibiteur.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATION
Contre-indication:
- sauf avec le ritonavir.
Augmentation des concentrations plasmatiques de la bithérapie par
diminution de son métabolisme hépatique par l’inhibiteur.
+ OXYCODONE
Association DECONSEILLEE
Surveillance clinique et adaptation éventuelle de la posologie de
l’oxycodone pendant le traitement par l'inhibiteur et après son arrêt.
Majoration des effets indésirables, notamment respiratoires, de
l’oxycodone par diminution de son métabolisme par l'inhibiteur.
+ PANOBINOSTAT
Précaution d'emploi
Surveillance clinique et ECG. Débuter le traitement à dose réduite de
moitié (10 mg).
Risque de majoration des effets indésirables, notamment
cardiaques, du panobinostat par diminution de son métabolisme
par l’inhibiteur.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ QUETIAPINE
CONTRE-INDICATIONAugmentation importante des concentrations de quétiapine, avec
risque de surdosage.
+ QUININE
ASDEC - PE
Association déconseillée :
- avec les inhibiteurs de protéases
Précaution d’emploi :
- avec les azolés antifongiques, certains macrolides, le tucatinib.
Surveillance clinique et ECG. Adaptation éventuelle de la posologie de
la quinine pendant le traitement par l’inhibiteur enzymatique et après
son arrêt.
Risque de majoration des effets indésirables de la quinine,
notamment troubles du rythme ventriculaire et troubles
neurosensoriels (cinchonisme).
+ RANOLAZINE
CONTRE-INDICATIONAugmentation des concentrations de ranolazine par diminution de
son métabolisme par l'inhibiteur.
+ RÉGORAFÉNIB
Association DECONSEILLEEAugmentation des concentrations plasmatiques de régorafenib par
diminution de son métabolisme hépatique par l’inhibiteur.
+ RIOCIGUAT
Association DECONSEILLEEAugmentation des concentrations plasmatiques de riociguat par
diminution de son métabolisme hépatique par l’inhibiteur.
+ RIVAROXABAN
Association DECONSEILLEEAugmentation des concentrations plasmatiques de rivaroxaban,
avec majoration du risque de saignement.
+ SILODOSINE
Association DECONSEILLEERisque d’augmentation des effets indésirables de la silodosine par
l’inhibiteur, notamment à type d’hypotension orthostatique.
+ SIMVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par diminution du métabolisme de la
simvastatine.
142
+ SUBSTRATS À RISQUE DU CYP3A4
A prendre en compteMajoration des effets indésirables propres à chaque substrat, avec
conséquences souvent sévères.
+ SUFENTANIL
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’analgésique
opiacé en cas de traitement par un inhibiteur puissant du CYP3A4.
Augmentation de l’effet dépresseur respiratoire de l’analgésique
opiacé par diminution de son métabolisme hépatique.
+ TAMSULOSINE
Association DECONSEILLEERisque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
+ TELITHROMYCINE
CONTRE-INDICATION
chez le patient insuffisant rénal ou hépatique sévère.
Risque de majoration des effets indésirables, notamment à type de
troubles du rythme cardiaque.
+ TICAGRELOR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de ticagrelor par
diminution de son métabolisme hépatique par l’inhibiteur.
+ TOLVAPTAN
Précaution d'emploi
Réduire la posologie des deux tiers aux trois quarts, selon la dose
prescrite.
Augmentation importante (entre 2 à 5 fois en moyenne) des
concentrations de tolvaptan, avec risque de majoration importante
des effets indésirables, notamment diurèse importante,
déshydratation, insuffisance rénale aiguë.
+ TRASTUZUMAB EMTANSINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques du DM1, un
composant du trastuzumab emtansine, par inhibition de son
métabolisme par l’inhibiteur.
+ TRÉTINOÏNE
Précaution d'emploi
Adaptation de la posologie de la trétinoïne pendant le traitement par
l’inhibiteur et après son arrêt.
Décrit pour les antifongiques azolés
Augmentation des concentrations de trétinoïne par diminution de
son métabolisme, avec risque de majoration de sa toxicité (pseudo-
tumor cerebrii, hypercalcémie…)
+ VÉNÉTOCLAX
CI - PE
Contre-indication :
- pendant la phase de titration.
Précaution d'emploi:
- réduction de posologie de 75% en phase de stabilisation.
Augmentation très importante des concentrations de vénétoclax par
diminution de son métabolisme hépatique, avec risque de
majoration de la toxicité, notamment hématologique.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique et ECG. S’il y a lieu, adaptation de la posologie du
vérapamil pendant le traitement par l’inhibiteur, et après son arrêt, le
cas échéant.
Bradycardie et/ou troubles de la conduction auriculo-ventriculaire,
par diminution du métabolisme hépatique du vérapamil par
l’inhibiteur.
+ VINCA-ALCALOÏDES CYTOTOXIQUES
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite.
Risque de majoration de la toxicité de l'antimitotique par diminution
de son métabolisme hépatique par l’inhibiteur.
+ ZOLPIDEM
A prendre en compteLégère augmentation de l'effet sédatif du zolpidem.
+ ZOPICLONE
A prendre en compteLégère augmentation de l'effet sédatif de la zopiclone.
INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
(citalopram, dapoxétine, escitalopram, fluoxetine, fluvoxamine, paroxetine, sertraline, vortioxétine)
+ ANTIAGRÉGANTS PLAQUETTAIRES
A prendre en compteAugmentation du risque hémorragique.
143
+ ANTICOAGULANTS ORAUX
A prendre en compteAugmentation du risque hémorragique.
+ ANTIDÉPRESSEURS IMIPRAMINIQUES
Précaution d'emploi
Surveillance clinique accrue et, si nécessaire, adaptation posologique.
Augmentation des concentrations plasmatiques de l'antidépresseur
imipraminique avec risque de convulsions et augmentation des
effets indésirables.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
A prendre en compteMajoration du risque hémorragique.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ CYPROHEPTADINE
A prendre en compteRisque de diminution de l'efficacité de l'antidépresseur.
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATION
Respecter un délai de deux semaines entre l'arrêt de l'IMAO et le début
du traitement par l'antidépresseur sérotoninergique, et d'au moins une
semaine entre l'arrêt de l'antidépresseur sérotoninergique (sauf pour la
fluoxétine : cinq semaines) et le début.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique très étroite.
Débuter l'association aux posologies minimales recommandées.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ IMAO-B
A prendre en compteRisque d'apparition d'un syndrome sérotoninergique.
+ LITHIUM
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ MILLEPERTUIS
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ ORLISTAT
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ TRAMADOL
A prendre en compteRisque d'apparition de convulsions et/ou d'un syndrome
sérotoninergique.
+ TRIPTANS
A prendre en compteRisque d'apparition d'un syndrome sérotoninergique.
INSULINE
+ ALCOOL (BOISSON OU EXCIPIENT)
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Augmentation de la réaction hypoglycémique (inhibition des
réactions de compensation pouvant faciliter la survenue de coma
hypoglycémique).
144
+ ANALOGUES DE LA SOMATOSTATINE
Précaution d'emploi
Prévenir le patient du risque d'hypoglycémie ou d'hyperglycémie,
renforcer l'autosurveillance glycémique et adapter si besoin la posologie
de l'insuline pendant le traitement par l'analogue de la somatostatine.
Risque d'hypoglycémie ou d'hyperglycémie : diminution ou
augmentation des besoins en insuline, par diminution ou
augmentation de la sécrétion de glucagon endogène.
+ BÊTA-2 MIMÉTIQUES
Précaution d'emploi
Renforcer la surveillance sanguine et urinaire.
Elévation de la glycémie par le bêta-2 mimétique.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêtabloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ CHLORPROMAZINE
Précaution d'emploi
Prévenir le patient et renforcer l'autosurveillance glycémique. Adapter
éventuellement la posologie de l'insuline pendant le traitement par le
neuroleptique et après son arrêt.
A fortes posologies (100 mg par jour de chlorpromazine) : élévation
de la glycémie (diminution de la libération de l'insuline).
+ DANAZOL
Association DECONSEILLEE
Si l'association ne peut être évitée, prévenir le patient et renforcer
l'autosurveillance glycémique. Adapter éventuellement la posologie de
l'insuline pendant le traitement par le danazol et après son arrêt.
Effet diabétogène du danazol.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Précaution d'emploi
Renforcer l'autosurveillance glycémique.
L'utilisation des IEC peut entraîner une majoration de l'effet
hypoglycémiant chez le diabétique traité par insuline. La survenue
de malaises hypoglycémiques semble exceptionnelle (amélioration
de la tolérance au glucose qui aurait pour conséquence une
réduction des besoins en insuline).
INTERFERON ALFA
+ FLUOROURACILE (ET, PAR EXTRAPOLATION, AUTRES FLUOROPYRIMIDINES)
A prendre en compteAugmentation de la toxicité gastro-intestinale du fluorouracile.
IPILIMUMAB
Voir aussi : anticorps monoclonaux (hors anti-TNF alpha)
+ ANTICOAGULANTS ORAUX
Précaution d'emploi
Surveillance clinique étroite.
Augmentation du risque d'hémorragies digestives.
IRINOTECAN
Voir aussi : cytotoxiques - substrats à risque du CYP3A4
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution probable des concentrations plasmatiques du
métabolite actif de l'irinotécan, avec risque d'échec du traitement
cytotoxique.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEERisque de majoration des effets indésirables de l’irinotécan par
augmentation des concentrations plasmatiques de son métabolite
actif.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques du métabolite actif de
l'irinotécan, avec risque d'échec du traitement cytotoxique.
145
ISAVUCONAZOLE
+ INDUCTEURS ENZYMATIQUES
CONTRE-INDICATIONDiminution des concentrations plasmatiques d’isavuconazole par
augmentation de son métabolisme hépatique par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
CI - PE
Contre-indication:
- avec le kétoconazole
Précaution d'emploi:
- avec les autres inhibiteurs puissants du CYP3A4
Augmentation des concentrations plasmatiques d’isavuconazole
par diminution de son métabolisme hépatique par l’inhibiteur.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques d’isavuconazole par
augmentation de son métabolisme hépatique par le millepertuis.
ISONIAZIDE
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ANESTHÉSIQUES VOLATILS HALOGÉNÉS
Précaution d'emploi
En cas d'intervention programmée, arrêter, par prudence, le traitement
par l'isoniazide une semaine avant l'intervention et ne le reprendre que
15 jours après.
Potentialisation de l'effet hépatotoxique de l'isonazide, avec
formation accrue de métabolites toxiques de l'isoniazide.
+ CARBAMAZEPINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage par inhibition de son métabolisme
hépatique.
+ DISULFIRAME
Association DECONSEILLEETroubles du comportement et de la coordination.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
Précaution d'emploi
Surveillance clinique et biologique.
Décrit pour la prednisolone. Diminution des concentrations
plasmatiques de l'isoniazide. Mécanisme invoqué : augmentation
du métabolisme hépatique de l'isoniazide et diminution de celui des
glucocorticoïdes.
+ KETOCONAZOLE
Précaution d'emploi
Espacer les prises des deux anti-infectieux d'au moins 12 heures.
Surveiller les concentrations plasmatiques du kétoconazole et adapter
éventuellement sa posologie.
Diminution des concentrations plasmatiques de kétoconazole.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique étroite, dosage des concentrations plasmatiques
de phénytoïne et adaptation éventuelle de sa posologie pendant le
traitement par l'isoniazide et après son arrêt.
Surdosage en phénytoïne (diminution de son métabolisme).
+ PYRAZINAMIDE
Précaution d'emploi
Surveillance clinique et biologique.
Addition des effets hépatotoxiques.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et biologique de cette association classique. En
cas d'hépatite, arrêter l'isoniazide.
Augmentation de l'hépatotoxicité de l'isoniazide (augmentation de
la formation de métabolites toxiques de l'isoniazide).
+ STAVUDINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
ISOPRENALINE
+ ANESTHÉSIQUES VOLATILS HALOGÉNÉS
Association DECONSEILLEETroubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
146
ITRACONAZOLE
Voir aussi : inhibiteurs puissants du CYP3A4
+ AFATINIB
Précaution d'emploi
Il est recommandé d’administrer l'itraconazole le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par l'itraconazole.
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ APREPITANT
A prendre en compteAugmentation des concentrations d’aprépitant par diminution de
son métabolisme hépatique par l’itraconazole.
+ ATORVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l'atorvastatine).
+ BUPRENORPHINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buprénorphine
pendant le traitement par l'inhibiteur et, le cas échéant, après son arrêt.
Augmentation des concentrations de buprénorphine par diminution
de son métabolisme hépatique, avec risque de majoration de ses
effets indésirables.
+ BUSPIRONE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique, avec majoration
importante de la sédation.
+ BUSULFAN
Association DECONSEILLEEAvec le busulfan à fortes doses : doublement des concentrations
de busulfan par l’itraconazole.
+ DABIGATRAN
CONTRE-INDICATIONAugmentation de plus du double des concentrations plasmatiques
de dabigatran, avec majoration du risque de saignement.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et, s'il y a lieu, de l'ECG et de la digoxinémie avec
adaptation de la posologie de la digoxine pendant le traitement par
l'itraconazole et après son arrêt.
Augmentation de la digoxinémie avec nausées, vomissements,
troubles du rythme.
+ ÉDOXABAN
Précaution d'emploi
Réduire la dose d’édoxaban de moitié.
Augmentation des concentrations plasmatiques de l’édoxaban,
avec majoration du risque de saignement.
+ ELVITÉGRAVIR
Précaution d'emploi
Avec l’elvitegravir co-administré avec le cobicistat, surveillance clinique.
Limiter la dose maximale d’itraconazole à 200 mg/j.
Augmentation des concentrations plasmatiques d’elvitegravir par
diminution de son métabolisme par l'itraconazole.
+ HYDROQUINIDINE
Précaution d'emploi
Surveillance des concentrations plasmatiques de l'antiarythmique et
diminution éventuelle de sa posologie si nécessaire.
Risque d'acouphènes et/ou de diminution de l'acuité auditive :
cinchonisme lié à une diminution du métabolisme hépatique de
l'antiarythmique par l'itraconazole.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
147
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations plasmatiques d’itraconazole, avec
risque de perte d’efficacité, par augmentation de son métabolisme
hépatique par l’inducteur.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique lors de l’association. L’administration de doses
élevées d’itraconazole (>200 mg par jour) n’est pas recommandée.
Risque d’augmentation des concentrations d’itraconazole par
l’inhibiteur de protéases.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution importante des concentrations plasmatiques
d’itraconazole, avec risque de perte d’efficacité, par augmentation
de son métabolisme hépatique par le millepertuis.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'itraconazole.
+ QUINIDINE
Précaution d'emploi
Surveillance clinique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes, ainsi que d'acouphènes et/ou de diminution de
l'acuité auditive (cinchonisme), par diminution du métabolisme
hépatique de la quinidine.
+ SALMETEROL
A prendre en compteAugmentation importante des concentrations de salmétérol par
diminution de son métabolisme hépatique par l'itraconazole.
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ TÉNOFOVIR ALAFÉNAMIDE
Précaution d'emploi
En cas de co-administration avec l’itraconazole, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ TRABECTÉDINE
Association DECONSEILLEE
Si l’association est nécessaire, surveillance clinique et adaptation
éventuelle de la posologie de la trabectedine pendant la durée du
traitement par l’itraconazole.
Risque d’augmentation des concentrations plasmatiques de la
trabectedine par l’itraconazole.
+ VENLAFAXINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
IVABRADINE
Voir aussi : bradycardisants
+ AZITHROMYCINE
Précaution d'emploi
Surveillance clinique et ECG pendant l’association.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes. De plus, risque d'augmentation des
concentrations plasmatiques de l’ivabradine par augmentation de
son absorption par l’azithromycine.
+ DILTIAZEM
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l’ivabradine et
de ses effets indésirables, notamment cardiaques (inhibition de son
métabolisme hépatique par le diltiazem), qui s’ajoutent aux effets
bradycardisants de ces substances.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’ivabradine
pendant l’association et après l’arrêt de l’inducteur.
Risque de diminution de l'efficacité de l’ivabradine, par
augmentation de son métabolisme par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l’ivabradine et
par conséquent de ses effets indésirables (inhibition de son
métabolisme hépatique par l’inhibiteur).
148
+ JOSAMYCINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'ivabradine et
par conséquent de ses effets indésirables (inhibition de son
métabolisme hépatique par la josamycine).
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution de l'efficacité de l’ivabradine, par
augmentation de son métabolisme par le millepertuis.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l’ivabradine et
de ses effets indésirables (inhibition de son métabolisme intestinal
par le pamplemousse).
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’ivabradine
pendant l’association et après l’arrêt de la rifampicine.
Risque de diminution de l'efficacité de l’ivabradine, par
augmentation de son métabolisme par la rifampicine.
+ VERAPAMIL
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l’ivabradine et
de ses effets indésirables, notamment cardiaques (augmentation
de son absorption et inhibition de son métabolisme hépatique par le
vérapamil), qui s’ajoutent aux effets bradycardisants de ces deux
médicaments.
IVACAFTOR (SEUL OU ASSOCIÉ)
(élexacaftor, ivacaftor, lumacaftor, tézacaftor)
+ FLUCONAZOLE
Précaution d'emploi
Se référer à l'AMM pour les adaptations posologiques.
Augmentation des concentrations d’ivacaftor, avec risque de
majoration des effets indésirables.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution importante des concentrations de l’ivacaftor, avec
risque de perte d’efficacité.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Se référer à l'AMM pour les adaptations posologiques.
Augmentation des concentrations d’ivacaftor, avec risque de
majoration des effets indésirables.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques
d’ivacaftor par le jus de pamplemousse.
JOSAMYCINE
Voir aussi : macrolides (sauf spiramycine)
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et, si besoin, dosage plasmatique et réduction
éventuelle de la posologie de la carbamazépine.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage, par diminution de son métabolisme
hépatique.
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ DISOPYRAMIDE
Précaution d'emploi
Surveillance clinique, biologique et électrocardiographique régulière.
Risque de majoration des effets indésirables du disopyramide :
hypoglycémies sévères, allongement de l’intervalle QT et troubles
du rythme ventriculaire graves, notamment à type de torsades de
pointes.
+ HALOFANTRINE
Association DECONSEILLEE
Si cela est possible, interrompre le macrolide. Si l’association ne peut
être évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
149
+ IVABRADINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'ivabradine et
par conséquent de ses effets indésirables (inhibition de son
métabolisme hépatique par la josamycine).
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SILDENAFIL
Précaution d'emploi
Débuter le traitement par sildénafil à la dose minimale en cas
d'association avec la josamycine.
Augmentation des concentrations plasmatiques de sildénafil, avec
risque d'hypotension.
+ TACROLIMUS
Association DECONSEILLEEAugmentation des concentrations sanguines de tacrolimus et de la
créatininémie, par inhibition du métabolisme hépatique du
tacrolimus par la josamycine.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
A prendre en compteRisque d'augmentation de la théophyllinémie, particulièrement chez
l'enfant.
KETAMINE
+ TICLOPIDINE
A prendre en compteAugmentation des concentrations plasmatiques de kétamine par
diminution de son métabolisme par la ticlopidine.
KETOCONAZOLE
Voir aussi : antabuse (réaction) - inhibiteurs puissants du CYP3A4
+ AFATINIB
Précaution d'emploi
Il est recommandé d’administrer le kétoconazole le plus à distance
possible de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par le kétoconazole.
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compteDiminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ ATORVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l'atorvastatine).
+ BUPRENORPHINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buprénorphine
pendant le traitement par l'inhibiteur et, le cas échéant, après son arrêt.
Augmentation des concentrations de buprénorphine par diminution
de son métabolisme hépatique, avec risque de majoration de ses
effets indésirables.
+ DABIGATRAN
CONTRE-INDICATIONAugmentation de plus du double des concentrations plasmatiques
de dabigatran, avec majoration du risque de saignement.
+ ELVITÉGRAVIR
Précaution d'emploi
Avec l’elvitegravir co-administré avec le cobicistat, surveillance clinique.
Limiter la dose maximale de kétoconazole à 200 mg/j.
Augmentation des concentrations plasmatiques d’elvitegravir par
diminution de son métabolisme par le kétoconazole.
+ FIDAXOMICINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
150
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ ISONIAZIDE
Précaution d'emploi
Espacer les prises des deux anti-infectieux d'au moins 12 heures.
Surveiller les concentrations plasmatiques du kétoconazole et adapter
éventuellement sa posologie.
Diminution des concentrations plasmatiques de kétoconazole.
+ LERCANIDIPINE
Association DECONSEILLEERisque majoré d'effets indesirables, notamment d'oedèmes, par
diminution du métabolisme hépatique de la dihydropyridine.
+ NEVIRAPINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de névirapine par
diminution de son métabolisme hépatique par le kétoconazole,
d'une part, et diminution des concentrations plasmatiques du
kétoconazole par augmentation de son métabolisme hépatique par
la névirapine, d'autre part.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par le kétoconazole.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l'efficacité des
deux anti-infectieux (induction enzymatique par la rifampicine et
diminution de l'absorption intestinale par l’azolé antifongique).
+ SALMETEROL
A prendre en compteAugmentation importante des concentrations de salmétérol par
diminution de son métabolisme hépatique par le kétoconazole.
+ TÉNOFOVIR ALAFÉNAMIDE
Précaution d'emploi
En cas de co-administration avec le kétoconazole, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ VENLAFAXINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
LAMIVUDINE
+ CLADRIBINE
Association DECONSEILLEERisque de diminution de l’efficacité de la cladribine par la
lamivudine.
+ SORBITOL
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance plus fréquente de la
charge virale.
Diminution des concentrations plasmatiques de lamivudine par le
sorbitol.
LAMOTRIGINE
Voir aussi : anticonvulsivants métabolisés
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
carbamazépine.
Risque d'augmentation des effets neurologiques (vertiges, ataxie,
diplopie) de la carbamazépine lors de l'introduction de la
lamotrigine.
+ ESTROPROGESTATIFS CONTRACEPTIFS
ASDEC - PE
Association déconseillée:
- Eviter de mettre en route une contraception orale pendant la période
d'ajustement posologique de la lamotrigine.
Précaution d'emploi:
- Surveillance clinique et adaptation de la posologie de la lamotrigine
lors de la mise en route d'une contraception orale et après son arrêt.
Diminution des concentrations et de l’efficacité de la lamotrigine par
augmentation de son métabolisme hépatique.
151
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
ASDEC - PE
Association déconseillée
- Eviter de mettre en route le traitement par ritonavir pendant la période
d’ajustement posologique de la lamotrigine.
Précaution d'emploi
- Surveillance clinique et adaptation de la posologie de la lamotrigine
lors de la mise en route du traitement par ritonavir.
Risque de diminution des concentrations et de l’efficacité de la
lamotrigine par augmentation de son métabolisme hépatique par le
ritonavir.
+ OXCARBAZEPINE
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques, avec
adaptation de la posologie de la lamotrigine si besoin.
Diminution des concentrations de la lamotrigine avec risque de
moindre efficacité, par augmentation de son métabolisme
hépatique par l'oxcarbazépine.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Association DECONSEILLEE
Si l'association s'avère nécessaire, surveillance clinique étroite.
Risque majoré de réactions cutanées graves (syndrome de Lyell).
Par ailleurs, augmentation des concentrations plasmatiques de
lamotrigine (diminution de son métabolisme hépatique par le
valproate de sodium).
LANSOPRAZOLE
Voir aussi : antisécrétoires inhibiteurs de la pompe à protons - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ TACROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines du tacrolimus, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après son arrêt.
Augmentation des concentrations sanguines du tacrolimus.
LAPATINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés - substrats à risque du CYP3A4
+ TÉDIZOLIDE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
lapatinib, par augmentation de son absorption avec le tédizolide
administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
LAXATIFS (TYPE MACROGOL)
(macrogol
+ MÉDICAMENTS ADMINISTRÉS PAR VOIE ORALE
A prendre en compte
Eviter la prise d’autres médicaments pendant et après l’ingestion dans
un délai d’au moins 2 h après la prise du laxatif, voire jusqu’à la
réalisation de l’examen.
Avec les laxatifs, notamment en vue d’explorations endoscopiques:
risque de diminution de l’efficacité du médicament administré avec
le laxatif.
LÉDIPASVIR
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
Précaution d'emploi
Il est recommandé de prendre l'’inhibiteur de la pompe à protons et le
lédipasvir simultanément.
Diminution des concentrations du lédipasvir en cas d’administration
de l’inhibiteur de la pompe à protons avant le lédipasvir.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
CONTRE-INDICATIONDiminution importante des concentrations plasmatiques du
lédipasvir par augmentation de son métabolisme hépatique par
l'inducteur enzymatique.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
CI - PE
Contre-indication :
- avec la rosuvastatine.
Précaution d'emploi :
- avec les autres inhibiteurs de l'HMG Co-A réductase.
Surveillance clinique et biologique. Adaptation éventuelle de la
posologie de la statine.
Risque d’augmentation des concentrations plasmatiques de la
statine et de ses effets indésirables à type de rhabdomyolyse.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution importante des concentrations plasmatiques
du lédipasvir par augmentation de son métabolisme hépatique par
le millepertuis.
+ RIFABUTINE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de lédipasvir par la
rifabutine, avec possible retentissement sur l’efficacité.
152
+ RIFAMPICINE
CONTRE-INDICATIONDiminution importante des concentrations plasmatiques du
lédipasvir par augmentation de son métabolisme hépatique par la
rifampicine.
+ TENOFOVIR DISOPROXIL
Précaution d'emploi
Surveillance clinique et biologique, notamment de la fonction rénale.
Lors de sa co-administration avec un inhibiteur de protéase,
augmentation des concentrations plasmatiques du ténofovir par le
lédipasvir.
LÉNACAPAVIR
+ ATAZANAVIR
Association DECONSEILLEELorsqu’il est associé au cobicistat, l’atazanavir provoque une
augmentation très importante des concentrations de lénacapavir.
+ EFAVIRENZ
Association DECONSEILLEEDiminution importante des concentrations de lénacapavir.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
+ OXCARBAZEPINE
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
+ RIFAMPICINE
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
LENALIDOMIDE
Voir aussi : médicaments à l'origine d'atteintes musculaires
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Précaution d'emploi
Renforcer le contrôle clinique et biologique, notamment durant les
premières semaines de traitement.
Risque majoré de survenue de rhabdomyolyses.
LERCANIDIPINE
Voir aussi : antagonistes des canaux calciques - antihypertenseurs sauf alpha-bloquants - dihydropyridines - médicaments abaissant la pression artérielle
+ CICLOSPORINE
Précaution d'emploi
Décaler les prises des deux médicaments. Dosage des concentrations
sanguines de l'immunosuppresseur, et adaptation si nécessaire de sa
posologie pendant l'association et après son arrêt.
Augmentation modérée des concentrations sanguines de
l'immunosuppresseur et augmentation plus notable des
concentrations de lercanidipine.
+ KETOCONAZOLE
Association DECONSEILLEERisque majoré d'effets indesirables, notamment d'oedèmes, par
diminution du métabolisme hépatique de la dihydropyridine.
+ PAMPLEMOUSSE (JUS ET FRUIT)
A prendre en compteRisque majoré d'effets indésirables, notamment d'oedèmes, par
diminution du métabolisme intestinal de la dihydropyridine.
LÉTERMOVIR
Voir aussi : inducteurs enzymatiques
+ ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
CONTRE-INDICATIONRisque de vasoconstriction coronaire ou des extrémités
(ergotisme), ou de poussées hypertensives.
153
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Surveillance clinique et biologique renforcée.
Augmentation, éventuellement très importante, des concentrations
sanguines de l'immunosuppresseur par inhibition de son
métabolisme et de la créatininémie.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
ASDEC - PE
Association déconseillée:
- avec simvastatine, pitavastatine, rosuvastatine
Précaution d'emploi (en cas d’utilisation du létermovir seul):
- ne pas dépasser 20 mg/ jour d’atorvastatine
- adaptation éventuelle de la posologie de fluvastatine et de
pravastatine,
Risque d’augmentation des concentrations plasmatiques de la
statine et de ses effets indésirables à type de rhabdomyolyse.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ VORICONAZOLE
Association DECONSEILLEE
Si l’association s’avère nécessaire, surveillance clinique étroite,
notamment les deux premières semaines après l’instauration ou l’arrêt
du traitement par létermovir.
Diminution de plus de la moitié de l’exposition du voriconazole.
LEVOCARNITINE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la lévocarnitine et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique
LEVODOPA
Voir aussi : médicaments à l'origine d'une hypotension orthostatique
+ BACLOFENE
A prendre en compteRisque d’aggravation du syndrome parkinsonien ou d’effets
indésirables centraux (hallucinations visuelles, état confusionnel,
céphalées).
+ FER
Précaution d'emploi
Prendre les sels de fer à distance de la lévodopa (plus de 2 heures si
possible).
Diminution de l'absorption digestive de la lévodopa.
+ IMAO-B
A prendre en compteAugmentation du risque d'hypotension orthostatique.
+ METHYLDOPA
Précaution d'emploi
Surveillance clinique et éventuellement diminution des doses de
lévodopa.
Augmentation des effets de la lévodopa mais également de ses
effets indésirables. Majoration de l'effet antihypertenseur de la
méthyldopa.
+ NEUROLEPTIQUES ANTIÉMÉTIQUES
CONTRE-INDICATION
Utiliser un antiémétique dénué d'effets extrapyramidaux.
Antagonisme réciproque entre la lévodopa et le neuroleptique.
+ NEUROLEPTIQUES ANTIPSYCHOTIQUES (SAUF CLOZAPINE)
Association DECONSEILLEE
Chez le patient parkinsonien, utiliser les doses minimales efficaces de
chacun des deux médicaments.
Antagonisme réciproque de la lévodopa et des neuroleptiques.
+ RESERPINE
CONTRE-INDICATIONInhibition des effets de la lévodopa.
+ SPIRAMYCINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
lévodopa.
En cas d'association avec la carbidopa : inhibition de l'absorption
de la carbidopa avec diminution des concentrations plasmatiques
de la lévodopa.
154
+ TETRABENAZINE
Association DECONSEILLEEAntagonisme réciproque entre la lévodopa et la tétrabénazine.
LEVOFLOXACINE
Voir aussi : fluoroquinolones - médicaments abaissant le seuil épileptogène - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et
adsorbants
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
LEVONORGESTREL
Voir aussi : progestatifs contraceptifs
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
En cas de prise d’un médicament inducteur dans les 4 dernières
semaines, l’utilisation d’une contraception d’urgence non hormonale
(DIU au cuivre) devrait s’envisager.
Si ce n’est pas possible, le doublement de la dose de lévonorgestrel est
une autre option.
Avec le lévonorgestrel utilisé dans l’indication contraception
d’urgence, diminution importante des concentrations plasmatiques
de lévonorgestrel, avec risque d’inefficacité.
LIDOCAINE
Voir aussi : antiarythmiques
+ AMIODARONE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations plasmatiques de lidocaïne. Si besoin, adaptation de la
posologie de la lidocaïne pendant le traitement par amiodarone et après
son arrêt.
Risque d’augmentation des concentrations plasmatiques de
lidocaïne, avec possibilité d’effets indésirables neurologiques et
cardiaques, par diminution de son métabolisme hépatique par
l’amiodarone.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations plasmatiques de lidocaïne pendant l'association et après
l'arrêt du bêta-bloquant. Adaptation si besoin de la posologie de la
lidocaïne.
Avec la lidocaïne utilisée par voie IV : augmentation des
concentrations plasmatiques de lidocaïne avec possibilité d'effets
indésirables neurologiques et cardiaques (diminution de la
clairance hépatique de la lidocaïne).
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
A prendre en compteEffet inotrope négatif avec risque de décompensation cardiaque.
+ CIMETIDINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement des concentrations
plasmatiques de la lidocaïne ; s'il y a lieu, adaptation de la posologie de
la lidocaïne pendant le traitement par la cimétidine et après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations plasmatiques de
lidocaïne avec risque d'effets indésirables neurologiques et
cardiaques (inhibition du métabolisme hépatique de la lidocaïne).
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle des
concentrations plasmatiques de la lidocaïne pendant et après l’arrêt de
l’association. Adaptation, si besoin, de la posologie de la lidocaïne.
Augmentation des concentrations plasmatiques de la lidocaïne
avec possibilités d’effets indésirables neurologiques et cardiaques
(diminution de la clairance hépatique de la lidocaïne).
LINCOSANIDES
(clindamycine, lincomycine)
+ CURARES
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
LINEZOLIDE
Voir aussi : IMAO-A réversibles, y compris oxazolidinones et bleu de méthylène - médicaments à l'origine d'un syndrome sérotoninergique
+ CLARITHROMYCINE
A prendre en compteRisque de majoration des effets indésirables du linézolide par la
clarithromycine, par augmentation de son absorption.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et augmentation éventuelle de la posologie du
linézolide pendant le traitement par la rifampicine.
Risque de diminution de l'efficacité du linézolide par augmentation
de son métabolisme hépatique par la rifampicine.
155
LITHIUM
Voir aussi : médicaments à l'origine d'un syndrome sérotoninergique
+ ACETAZOLAMIDE
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
Association DECONSEILLEE
Si l'usage d'un antagoniste de l'angiotensine II est indispensable,
surveillance stricte de la lithémie et adaptation de la posologie.
Augmentation de la lithémie pouvant atteindre des valeurs toxiques
(diminution de l'excrétion rénale du lithium).
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Association DECONSEILLEE
Si l'association ne peut être évitée, surveiller étroitement la lithémie et
adapter la posologie du lithium pendant l'association et après l'arrêt de
l'anti-inflammatoire non stéroïdien.
Augmentation de la lithémie pouvant atteindre des valeurs toxiques
(diminution de l'excrétion rénale du lithium).
+ CAFEINE
A prendre en compteEn cas d’arrêt brutal de la consommation de café ou de
médicaments contenant de la caféine, risque d’augmentation de la
lithémie.
+ CALCITONINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d’association.
Risque de baisse de l’efficacité du lithium par augmentation de son
élimination rénale par la calcitonine.
+ CARBAMAZEPINE
Association DECONSEILLEERisque de neurotoxicité se manifestant par des troubles
cérébelleux, confusion, somnolence, ataxie. Ces troubles sont
réversibles à l'arrêt du traitement par le lithium.
+ DIURÉTIQUES DE L'ANSE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance stricte de la lithémie et
adaptation de la posologie du lithium.
Augmentation de la lithémie avec signes de surdosage en lithium,
comme lors d’un régime désodé (diminution de l’excrétion urinaire
du lithium).
+ DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Augmentation de la lithémie avec signes de surdosage en lithium,
comme lors d’un régime désodé (diminution de l’excrétion urinaire
du lithium).
+ DIURÉTIQUES THIAZIDIQUES ET APPARENTÉS
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance stricte de la lithémie et
adaptation de la posologie du lithium.
Augmentation de la lithémie avec signes de surdosage en lithium,
comme lors d’un régime désodé (diminution de l’excrétion urinaire
du lithium).
+ GLYCEROL
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Association DECONSEILLEE
Si l'usage d'un IEC est indispensable, surveillance stricte de la lithémie
et adaptation de la posologie du lithium.
Augmentation de la lithémie pouvant atteindre des valeurs toxiques
(diminution de l'excrétion rénale du lithium).
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ MANNITOL
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
+ METHYLDOPA
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de lithium.
Augmentation de la lithémie pouvant atteindre des valeurs
toxiques, avec signes de surdosage en lithium.
156
+ METRONIDAZOLE
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Augmentation de la lithémie pouvant atteindre des valeurs
toxiques, avec signes de surdosage en lithium.
+ NEUROLEPTIQUES
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d’apparition de signes neuropsychiques évocateurs d’un
syndrome malin des neuroleptiques ou d’une intoxication au lithium.
+ ORLISTAT
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ SODIUM (BICARBONATE DE)
Précaution d'emploi
Eviter les surcharges sodées et tenir compte de la présence de sodium
dans certains médicaments comme les antiacides.
Risque de baisse de l’efficacité du lithium par augmentation de son
élimination rénale par les sels de sodium.
+ SODIUM (CHLORURE DE)
Précaution d'emploi
Eviter les surcharges sodées et tenir compte de la présence de sodium
dans certains médicaments comme les antiacides.
Risque de baisse de l’efficacité du lithium par augmentation de son
élimination rénale par les sels de sodium.
+ THEOPHYLLINE
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
+ TOPIRAMATE
Précaution d'emploi
Surveillance clinique et biologique. Adaptation de la posologie du lithium.
Pour des doses de topiramate >= 200 mg par jour : augmentation
de la lithémie pouvant atteindre des valeurs toxiques, avec signes
de surdosage en lithium.
LOMITAPIDE
+ DILTIAZEM
CONTRE-INDICATIONAugmentation des concentrations de lomitapide, avec risque
d’hépatotoxicité.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du lomitapide par
diminution de son métabolisme hépatique par l’inhibiteur.
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution des concentrations plasmatiques du
lomitapide.
LOMUSTINE
Voir aussi : cytotoxiques
+ CIMETIDINE
Association DECONSEILLEEAvec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : toxicité médullaire accrue (inhibition du métabolisme de
la lomustine).
LOSARTAN
Voir aussi : antagonistes des récepteurs de l'angiotensine II - antihypertenseurs sauf alpha-bloquants - hyperkaliémiants - médicaments abaissant la pression
artérielle - médicaments, bradykinine et angio-œdème
+ FLUCONAZOLE
A prendre en compteRisque de diminution de l’efficacité du losartan, par inhibition de la
formation de son métabolite actif par le fluconazole.
157
LUMEFANTRINE
Voir aussi : antiparasitaires susceptibles de donner des torsades de pointes - substances susceptibles de donner des torsades de pointes - substrats à risque du
CYP3A4
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si cela est possible, interrompre l’inhibiteur. Si l’association ne peut être
évitée, contrôle préalable du QT et surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
LURASIDONE
+ INDUCTEURS ENZYMATIQUES
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la lurasidone par
augmentation de son métabolisme hépatique par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la lurasidone
par diminution de son métabolisme hépatique par l’inhibiteur.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la lurasidone par
augmentation de son métabolisme hépatique par le millepertuis.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la lurasidone
par diminution de son métabolisme par le pamplemousse.
MACITENTAN
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations plasmatiques de macitentan par
augmentation de son métabolisme par l’inducteur.
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
macitentan par augmentation de son métabolisme par le
millepertuis.
MACROLIDES (SAUF SPIRAMYCINE)
(azithromycine, clarithromycine, erythromycine, josamycine, midecamycine, roxithromycine, telithromycine)
+ ALCALOÏDES DE L'ERGOT DE SEIGLE DOPAMINERGIQUES
Association DECONSEILLEEAugmentation des concentrations plasmatiques du dopaminergique
avec accroissement possible de son activité ou apparition de
signes de surdosage.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par le macrolide et après son
arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ COLCHICINE
CONTRE-INDICATIONAugmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par le macrolide et après son arrêt.
Augmentation de la digoxinémie par augmentation de son
absorption.
+ DIHYDROERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition de
l’élimination hépatique de l'alcaloïde de l’ergot de seigle).
+ ERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (diminution
de l'élimination hépatique de l'ergotamine).
158
MAGNÉSIUM
+ INHIBITEURS D'INTÉGRASE
Précaution d'emploi
Prendre les sels de magnésium à distance de l’antirétroviral (plus de 2
heures, si possible).
Diminution de l'absorption digestive des inhibiteurs d’intégrase.
+ ROXADUSTAT
Précaution d'emploi
Prendre le roxadustat à distance des sels de magnésium (plus de 1
heure, si possible).
La prise de cation divalent peut diminuer l’absorption intestinale et,
potentiellement, l’efficacité du roxadustat pris simultanément.
MANNITOL
+ LITHIUM
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
MARAVIROC
+ FOSAMPRENAVIR
Association DECONSEILLEEDiminution significative des concentrations d’amprénavir pouvant
conduire à une perte de la réponse virologique.
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
La dose de maraviroc doit être augmentée à 600 mg deux fois par jour
dans cette situation.
En l’absence de co-administration avec un inhibiteur puissant du
CYP3A4, diminution des concentrations de maraviroc par
l’inducteur (sauf la névirapine).
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
La dose de maraviroc doit être diminuée à 150 mg deux fois par jour en
cas de co-administration avec cet inhibiteur.
A l'exception du tipranavir boosté par ritonavir où la dose de maraviroc
doit être de 300 mg deux fois par jour.
Augmentation des concentrations de maraviroc par l’inhibiteur.
+ MILLEPERTUIS
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
maraviroc pouvant conduire à une perte de la réponse virologique.
MARIBAVIR
+ GANCICLOVIR
CONTRE-INDICATIONAntagonisme de la phosporylation et donc de l'effet
pharmacologique du ganciclovir par le maribavir.
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation éventuelle de la posologie
pendant l'association et après son arrêt.
Possible augmentation des concentrations de
l’immunosuppresseur.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEE
Si l’association ne peut être évitée, augmentation éventuelle de la
posologie de maribavir.
Diminution possiblement importante des concentrations de
maribavir avec la rifampicine, avec risque de réduction de la
réponse virologique.
+ VALGANCICLOVIR
CONTRE-INDICATIONAntagonisme de la phosporylation et donc de l'effet
pharmacologique du valganciclovir par le maribavir.
MÉDICAMENTS À L'ORIGINE D'ATTEINTES MUSCULAIRES
Certains médicaments présentent une toxicité musculaire qui peut conjuguer des crampes, une faiblesse, des douleurs parfois intenses (myalgies), voire la destruction
des fibres du muscle strié (rhabdomyolyse), avec atteinte du rein puis d’autres organes engageant le pronostic vital. L’association de plusieurs médicaments ayant ce
potentiel majore ce risque. Le dosage des CPK est impératif en cas de signes cliniques évocateurs.
(atorvastatine, bezafibrate, ciclosporine, ciprofibrate, colchicine, daptomycine, dasatinib, ezetimibe, fenofibrate, fluvastatine, gemfibrozil, imatinib, lenalidomide,
pitavastatine, pravastatine, rosuvastatine, simvastatine)
+ AUTRES MÉDICAMENTS À L'ORIGINE D'ATTEINTES MUSCULAIRES
A prendre en compteRisque de majoration des effets indésirables musculaires.
159
MÉDICAMENTS À L'ORIGINE D'UN HYPOGONADISME MASCULIN
(abiraterone, apalutamide, bicalutamide, cyproterone, dégarélix, dutasteride, enzalutamide, finasteride, flutamide, gosereline, leuproreline, nilutamide, triptoreline)
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
MÉDICAMENTS À L'ORIGINE D'UN SYNDROME SÉROTONINERGIQUE
Certains surdosages ou certains médicaments peuvent donner lieu à un syndrome sérotoninergique justifiant l'arrêt immédiat du traitement.
Ces médicaments sont essentiellement représentés par
- le linézolide
- le bleu de méthylène
- le millepertuis
- la péthidine et le tramadol
- la plupart des antidépresseurs
- la classe des inhibiteurs de la recapture de la sérotonine,
- certains tricycliques (clomipramine, amitriptyline, imipramine, trimipramine)
- les mixtes (venlafaxine, milnacipran, sibutramine)
- avec indications d’autres que la dépression : duloxétine, oxitriptan)
- les IMAO, essentiellement non sélectifs, voire les IMAO-A sélectifs
Le syndrome sérotoninergique se manifeste par l'apparition (éventuellement brutale) simultanée ou séquentielle, d'un ensemble de symptômes pouvant nécessiter
l'hospitalisation, voire exceptionnellement entraîner le décès.
Ces symptômes peuvent être d'ordre :
- digestifs (diarrhée),
- neuropsychiques (agitation, confusion, hypomanie),
- moteurs (myoclonies, tremblements, hyperréflexie, rigidité, hyperactivité),
- végétatifs (variations tensionnelles, tachycardie, frissons, hyperthermie, sueurs, éventuellement coma).
Le strict respect des doses préconisées constitue un facteur essentiel dans la prévention de l'apparition de ce syndrome.
Le niveau de risque est très variable selon les associations. Le tableau est sévère, voire fatal, notamment avec les IMAO non sélectifs (se reporter aux interactions
contre-indiquées dans le Thesaurus).
(amitriptyline, bleu de methylene, bupropion, citalopram, clomipramine, duloxetine, escitalopram, fluoxetine, fluvoxamine, imipramine, iproniazide, linezolide, lithium,
millepertuis, milnacipran, moclobemide, oxitriptan, paroxetine, pethidine, sertraline, tramadol, trimipramine, tryptophane, venlafaxine)
+ AUTRES MÉDICAMENTS À L'ORIGINE D'UN SYNDROME SÉROTONINERGIQUE
A prendre en compteRisque d'apparition ou de majoration d'un syndrome
sérotoninergique en cas d'association de ces médicaments.
MÉDICAMENTS À L'ORIGINE D'UNE HYPOTENSION ORTHOSTATIQUE
Outre les antihypertenseurs, de nombreux médicaments peuvent entraîner une hypotension orthostatique. C'est le cas notamment des dérivés nitrés, des inhibiteurs
de la phosphodiestérase de type 5, des alpha-bloquants à visée urologique, des antidépresseurs imipraminiques et des neuroleptiques phénothiaziniques, des
agonistes dopaminergiques et de la lévodopa. Leur utilisation conjointe risque donc de majorer la fréquence et l’intensité de cet effet indésirable. Se reporter aux
interactions propres à chaque classe, avec les niveaux de contrainte correspondants.
(alfuzosine, alimemazine, alizapride, amantadine, amifostine, amisulpride, amitriptyline, amoxapine, apomorphine, aripiprazole, avanafil, baclofene, bromocriptine,
chlorpromazine, clomipramine, clozapine, cyamemazine, dinitrate d'isosorbide, dosulepine, doxazosine, doxepine, droperidol, entacapone, flupentixol, fluphenazine,
haloperidol, imipramine, isosorbide, levodopa, levomepromazine, lévosimendan, lisuride, loxapine, maprotiline, metopimazine, molsidomine, nicorandil, olanzapine,
oxomemazine, paliperidone, penfluridol, périndopril, pimozide, pipamperone, pipotiazine, piribedil, pramipexole, prazosine, promethazine, propericiazine, quetiapine,
rasagiline, riociguat, risperidone, ropinirole, rotigotine, selegiline, sildenafil, silodosine, sulpiride, tadalafil, tamsulosine, terazosine, tiapride, tolcapone, trimipramine,
trinitrine, vardenafil, vortioxétine, zuclopenthixol)
+ DAPOXÉTINE
ASDEC - APEC
Association déconseillée
- avec les inhibiteurs de la phosphodiestérase de type 5
A prendre en compte
- avec les autres classes thérapeutiques
Risque de majoration des effets indésirables, notamment à type de
vertiges ou de syncopes.
+ MÉDICAMENTS ABAISSANT LA PRESSION ARTÉRIELLE
A prendre en compteRisque de majoration d’une hypotension, notamment orthostatique.
MÉDICAMENTS À RISQUE LORS DU SEVRAGE TABAGIQUE
(clozapine, methadone, ropinirole, theophylline)
+ TRAITEMENTS DE SUBSTITUTION NICOTINIQUE
A prendre en compteRisque de surdosage lors du remplacement du tabac par le
traitement substitutif.
160
MÉDICAMENTS ABAISSANT LA PRESSION ARTÉRIELLE
(acebutolol, altizide, amiloride, amlodipine, atenolol, azilsartan, benazepril, bendroflumethiazide, betaxolol, bisoprolol, bumetanide, candesartan cilexetil, canrenoate de
potassium, captopril, carteolol, carvedilol, celiprolol, chlortalidone, cicletanine, cilazapril, clévidipine, clonidine, clopamide, cyclothiazide, dihydralazine, diltiazem,
doxazosine, enalapril, eplerenone, eprosartan, felodipine, fosinopril, furosemide, guanfacine, hydrochlorothiazide, indapamide, irbesartan, isradipine, labetalol,
lacidipine, lercanidipine, levobunolol, lisinopril, losartan, manidipine, methyclothiazide, methyldopa, metoprolol, moexipril, moxonidine, nadolol, nebivolol, nicardipine,
nifedipine, nimodipine, nitrendipine, olmesartan, perindopril tert-butylamine, pindolol, piretanide, prazosine, propranolol, quinapril, ramipril, rilmenidine, sotalol,
spironolactone, tamsulosine, telmisartan, terazosine, tertatolol, timolol, trandolapril, triamterene, urapidil, valsartan, verapamil, zofenopril)
+ MÉDICAMENTS À L'ORIGINE D'UNE HYPOTENSION ORTHOSTATIQUE
A prendre en compteRisque de majoration d’une hypotension, notamment orthostatique.
MÉDICAMENTS ABAISSANT LE SEUIL ÉPILEPTOGÈNE
L'utilisation conjointe de médicaments proconvulsivants, ou abaissant le seuil épileptogène, devra être soigneusement pesée, en raison de la sévérité du risque
encouru. Ces médicaments sont représentés notamment par la plupart des antidépresseurs (imipraminiques, inhibiteurs sélectifs de la recapture de la sérotonine), les
neuroleptiques (phénothiazines et butyrophénones), la méfloquine, la chloroquine, les fluoroquinolones, le bupropion, le tramadol.
(alimemazine, amitriptyline, amoxapine, bupropion, camphre, chloroquine, chlorpromazine, cineole, ciprofloxacine, citalopram, clomipramine, cyamemazine,
dosulepine, doxepine, droperidol, enoxacine, escitalopram, eucalyptus, eugenol, fampridine, fluoxetine, fluphenazine, fluvoxamine, haloperidol, imipramine,
levofloxacine, levomenthol, levomepromazine, lomefloxacine, maprotiline, mefloquine, menthe, menthol racemique, moxifloxacine, niaouli, norfloxacine, ofloxacine,
oxomemazine, paroxetine, pefloxacine, penfluridol, pimozide, pipamperone, pipotiazine, promethazine, propericiazine, quetiapine, sertraline, tapentadol, terpine,
terpineol, terpinol, thymol, tramadol, trimipramine, vortioxétine)
+ AUTRES MÉDICAMENTS ABAISSANT LE SEUIL ÉPILEPTOGÈNE
A prendre en compteRisque accru de convulsions.
MÉDICAMENTS ATROPINIQUES
Il faut prendre en compte le fait que les substances atropiniques peuvent additionner leurs effets indésirables et entraîner plus facilement une rétention urinaire, une
poussée aiguë de glaucome, une constipation, une sécheresse de la bouche, etc…
Les divers médicaments atropiniques sont représentés par les antidépresseurs imipraminiques, la plupart des antihistaminiques H1 atropiniques, les antiparkinsoniens
anticholinergiques, les antispasmodiques atropiniques, le disopyramide, les neuroleptiques phénothiaziniques ainsi que la clozapine.
(alimemazine, amitriptyline, amoxapine, atropine, azelastine, biperidene, brompheniramine, chlorphenamine, chlorpromazine, clidinium, clomipramine, clozapine,
cyamemazine, cyclopentolate, cyproheptadine, darifenacine, dexchlorpheniramine, di(acefylline) diphenhydramine, dimenhydrinate, diphenhydramine, disopyramide,
dosulepine, doxepine, doxylamine, fesoterodine, flavoxate, flunarizine, flupentixol, fluphenazine, glycopyrronium, homatropine, hydroxyzine, imipramine, ipratropium,
isothipendyl, levomepromazine, loxapine, maprotiline, méclozine, mepyramine, mequitazine, metopimazine, nefopam, oxomemazine, oxybutynine, pheniramine,
phenyltoloxamine, pimethixene, pipotiazine, pizotifene, promethazine, propericiazine, quetiapine, quinidine, scopolamine, solifenacine, tolterodine, trihexyphenidyle,
trimipramine, triprolidine, tropatepine, tropicamide, trospium, uméclidinium, zuclopenthixol)
+ AUTRES MÉDICAMENTS ATROPINIQUES
A prendre en compteAddition des effets indésirables atropiniques à type de rétention
urinaire, constipation, sécheresse de la bouche….
+ ANTICHOLINESTÉRASIQUES
A prendre en compteRisque de moindre efficacité de l’anticholinestérasique par
antagonisme des récepteurs de l’acétylcholine par l’atropinique.
+ MORPHINIQUES
A prendre en compteRisque important d'akinésie colique, avec constipation sévère.
MÉDICAMENTS MÉTHÉMOGLOBINISANTS
(acetylsulfafurazol, benzocaïne, dapsone, flutamide, metoclopramide, prilocaine, sodium (nitroprussiate de), sulfadiazine, sulfadoxine, sulfafurazol, sulfaguanidine,
sulfamethizol, sulfamethoxazole)
+ AUTRES MÉDICAMENTS MÉTHÉMOGLOBINISANTS
A prendre en compteRisque d'addition des effets méthémoglobinisants.
MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
(amitriptyline, clomipramine, duloxetine, imipramine, milnacipran, oxitriptan, venlafaxine)
+ ADRÉNALINE (VOIE BUCCO-DENTAIRE OU SOUS-CUTANÉE)
Précaution d'emploi
Limiter l'apport, par exemple : moins de 0,1 mg d'adrénaline en 10
minutes ou 0,3 mg en 1 heure chez l'adulte.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ ANTIAGRÉGANTS PLAQUETTAIRES
A prendre en compteAugmentation du risque hémorragique.
161
+ ANTICOAGULANTS ORAUX
A prendre en compteAugmentation du risque hémorragique.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
A prendre en compteAugmentation du risque hémorragique.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATION
Respecter un délai de deux semaines entre l'arrêt de l'IMAO et le début
de l'autre traitement, et d'au moins une semaine entre l'arrêt de l'autre
traitement et le début de l'IMAO.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique très étroite.
Débuter l'association aux posologies minimales recommandées.
Risque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueur, confusion voire coma.
+ ORLISTAT
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ SYMPATHOMIMÉTIQUES ALPHA ET BÊTA (VOIE IM ET IV)
Association DECONSEILLEEHypertension paroxystique avec possibilité de troubles du rythme
(inhibition de l'entrée du sympathomimétique dans la fibre
sympathique).
MÉDICAMENTS NÉPHROTOXIQUES
L'utilisation conjointe de médicaments ayant une toxicité rénale propre augmente le risque de néphrotoxicité. Si une telle association est nécessaire, il faut renforcer la
surveillance biologique rénale.
Les médicaments concernés sont représentés notamment par les produits de contraste iodés, les aminosides, les organoplatines, le méthotrexate à fortes doses,
certains antiviraux (tels les "ciclovirs" ou le foscarnet), la pentamidine, la ciclosporine ou le tacrolimus.
(aciclovir, acide amidotrizoïque, acide clodronique, acide ioxaglique, acide ioxitalamique, adefovir, amikacine, amphotericine b, carboplatine, ciclosporine, cisplatine,
colistine, foscarnet, ganciclovir, gentamicine, ifosfamide, iobitridol, iodixanol, iohexol, iomeprol, iopamidol, iopromide, ioversol, isepamicine, methotrexate, netilmicine,
oxaliplatine, pentamidine, spectinomycine, streptomycine, streptozocine, tacrolimus, teicoplanine, tenofovir disoproxil, tobramycine, valaciclovir, valganciclovir,
vancomycine)
+ AUTRES MÉDICAMENTS NÉPHROTOXIQUES
A prendre en compteRisque de majoration de la néphrotoxicité.
MÉDICAMENTS OTOTOXIQUES
L'utilisation conjointe de médicaments ayant une ototoxicité augmente le risque d’atteinte cochléo-vestibulaire. Si une telle association est nécessaire, il convient de
renforcer la surveillance de la fonction auditive.
Les médicaments concernés sont, notamment, les glycopeptides tels que vancomycine et teicoplanine, les aminosides, les organoplatines et les diurétiques de l’anse.
(amikacine, bumetanide, carboplatine, cisplatine, furosemide, gentamicine, isepamicine, netilmicine, oxaliplatine, piretanide, streptomycine, teicoplanine, tobramycine,
vancomycine, vinblastine, vincristine, vindesine, vinflunine, vinorelbine)
+ AUTRES MÉDICAMENTS OTOTOXIQUES
A prendre en compteMajoration de l'ototoxicité.
162
MÉDICAMENTS SÉDATIFS
Il faut prendre en compte le fait que de nombreux médicaments ou substances peuvent additionner leurs effets dépresseurs du système nerveux central et contribuer à
diminuer la vigilance. Il s'agit des dérivés morphiniques (analgésiques, antitussifs et traitements de substitution), des neuroleptiques, des barbituriques, des
benzodiazépines, des anxiolytiques autres que les benzodiazépines (par exemple, le méprobamate), des hypnotiques, des antidépresseurs sédatifs (amitriptyline,
doxépine, miansérine, mirtazapine, trimipramine), des antihistaminiques H1 sédatifs, des antihypertenseurs centraux, du baclofène et du thalidomide.
(agomelatine, alfentanil, alimemazine, alizapride, alprazolam, amisulpride, amitriptyline, aripiprazole, avizafone, azelastine, baclofene, bromazepam, brompheniramine,
buprenorphine, captodiame, cénobamate, chlordiazepoxide, chlorphenamine, chlorpromazine, clobazam, clonazepam, clonidine, clorazepate, clotiazepam, clozapine,
codeine, cyamemazine, cyproheptadine, dapoxétine, dexchlorpheniramine, dexmédétomidine, dextromethorphane, di(acefylline) diphenhydramine, diazepam,
dihydrocodeine, dimenhydrinate, diphenhydramine, doxepine, doxylamine, droperidol, eskétamine, estazolam, eszopiclone, ethylmorphine, etifoxine, fenspiride,
fentanyl, flunarizine, flupentixol, fluphenazine, flurazepam, gabapentine, haloperidol, hydromorphone, hydroxyzine, isothipendyl, ketotifene, levomepromazine,
loflazépate, loprazolam, lorazepam, lormetazepam, loxapine, maprotiline, méclozine, mepyramine, mequitazine, methadone, methyldopa, metoclopramide,
metopimazine, mianserine, midazolam, mirtazapine, morphine, moxonidine, nalbuphine, naloxone, nefopam, nitrazepam, nordazepam, noscapine, olanzapine,
oxazepam, oxetorone, oxomemazine, oxybate de sodium, oxycodone, paliperidone, penfluridol, pérampanel, pethidine, pheniramine, phenobarbital, phenyltoloxamine,
pholcodine, pimethixene, pimozide, pipamperone, pipotiazine, pizotifene, prazepam, pregabaline, primidone, promethazine, propericiazine, quetiapine, remifentanil,
rilmenidine, risperidone, ropinirole, rupatadine, sodium (oxybate de), sufentanil, sulpiride, tapentadol, tetrabenazine, thalidomide, tiapride, tramadol, trimipramine,
triprolidine, ziconotide, zolpidem, zopiclone, zuclopenthixol)
+ AUTRES MÉDICAMENTS SÉDATIFS
CI - ASDEC - APEC
A prendre en compte:
- pour tous les médicaments sédatifs entre eux sauf:
- avec l'oxybate de sodium (association déconseillée)
- entre l'oxybate de sodium et les opiacés ou les barbituriques (contre-
indication)
Majoration de la dépression centrale.
L'altération de la vigilance peut rendre dangereuses la conduite de
véhicules et l'utilisation de machines.
+ ALCOOL (BOISSON OU EXCIPIENT)
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Majoration par l'alcool de l'effet sédatif de ces substances.
L'altération de la vigilance peut rendre dangereuses la conduite de
véhicules et l'utilisation de machines.
MÉDICAMENTS, BRADYKININE ET ANGIO-ŒDÈME
Certains médicaments ou classes thérapeutiques sont susceptibles de provoquer une réaction vasculaire à type d’angio-œdème de la face et du cou, résultant de
l’inhibition de la dégradation de la bradykinine. Les médicaments les plus fréquemment impliqués sont les IEC, certains immunosuppresseurs dits mTORi, un
antidiarrhéique, le racécadotril, un cytotoxique, l’estramustine, le sacubitril. Les antidiabétiques de la classe des gliptines ont été impliqués dans une étude isolée. Les
conséquences de l’angio-oedème peuvent parfois être fatales, par obstruction des voies respiratoires. L’angio-oedème peut survenir indépendamment d’une
association simultanée entre ces médicaments, au cas où le patient aurait été exposé antérieurement à l’un des deux protagonistes. Il conviendra de rechercher des
antécédents de survenue de cet effet et de mesurer la nécessité de ce type d’association.
(alteplase recombinante, azilsartan, benazepril, candesartan cilexetil, captopril, cilazapril, enalapril, eprosartan, estramustine, évérolimus, fosinopril, irbesartan,
linagliptine, lisinopril, losartan, moexipril, olmesartan, périndopril, quinapril, racecadotril, ramipril, sacubitril, saxagliptine, sirolimus, sitagliptine, telmisartan,
temsirolimus, trandolapril, valsartan, vildagliptine, zofenopril)
+ AUTRES MEDICAMENTS À RISQUE D'ANGIO-ŒDÈME
CI - ASDEC - APEC
Contre-indication :
- entre sacubitril et IEC
A prendre en compte :
- entre gliptines et IEC
Déconseillé entre les autres
Risque de majoration de la survenue d'un angio-œdème d'origine
bradykinique, pouvant être fatal.
MEFLOQUINE
Voir aussi : bradycardisants - médicaments abaissant le seuil épileptogène
+ QUININE
Association DECONSEILLEE
Respecter un délai minimum de 12 heures entre la fin de
l'administration IV de quinine et le début de l'administration de
méfloquine.
Pour la quinine administrée par voie IV : risque majoré de survenue
de crises épileptiques par addition des effets proconvulsivants.
MEQUITAZINE
Voir aussi : médicaments atropiniques - médicaments sédatifs - substances susceptibles de donner des torsades de pointes - torsadogènes (sauf arsénieux,
antiparasitaires, neuroleptiques, méthadone...)
+ BUPROPION
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ CINACALCET
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ DULOXETINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
163
+ FLUOXETINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ PAROXETINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ TERBINAFINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
METFORMINE
+ ALCOOL (BOISSON OU EXCIPIENT)
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Risque majoré d'acidose lactique lors d'intoxication alcoolique
aiguë, particulièrement en cas de jeûne ou dénutrition, ou bien
d'insuffisance hépatocellulaire.
+ DIURÉTIQUES DE L'ANSE
Précaution d'emploi
Ne pas utiliser la metformine lorsque la créatininémie dépasse 15 mg/l
(135 μmol/l) chez l'homme, et 12 mg/l (110 μmol/l) chez la femme.
Acidose lactique due à la metformine, déclenchée par une
éventuelle insuffisance rénale fonctionnelle, liée aux diurétiques de
l'anse.
+ DOLUTÉGRAVIR
Précaution d'emploi
Chez le patient avec une insuffisance rénale modérée, surveillance
clinique et éventuelle réduction supplémentaire de la posologie de
metformine.
Augmentation moyenne de moins de deux fois des concentrations
plasmatiques de metformine.
+ PRODUITS DE CONTRASTE IODÉS
CONTRE-INDICATION
Le traitement par la metformine doit être suspendu au moment de
l'examen radiologique pour n'être repris que 2 jours après.
Risque important d'acidose lactique par hémoconcentration de la
metformine, dans le cas d'un arrêt cardio-respiratoire induit par
l'examen radiologique, avec insuffisance rénale aiguë.
CONTRE-INDICATION
Le traitement par la metformine doit être suspendu au moment de
l'examen radiologique pour n'être repris que 2 jours après.
Risque important d'acidose lactique par hémoconcentration de la
metformine, dans le cas d'un arrêt cardio-respiratoire induit par
l'examen radiologique, avec insuffisance rénale aiguë.
CONTRE-INDICATION
Le traitement par la metformine doit être suspendu au moment de
l'examen radiologique pour n'être repris que 2 jours après.
Risque important d'acidose lactique par hémoconcentration de la
metformine, dans le cas d'un arrêt cardio-respiratoire induit par
l'examen radiologique, avec insuffisance rénale aiguë.
METHADONE
Voir aussi : morphiniques - morphiniques en traitement de substitution - médicaments sédatifs - médicaments à risque lors du sevrage tabagique - substances
susceptibles de donner des torsades de pointes
+ ANTITUSSIFS MORPHINE-LIKE
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ ANTITUSSIFS MORPHINIQUES VRAIS
A prendre en compteRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations de la
méthadone, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ CIMETIDINE
Précaution d'emploi
Surveillance clinique et électrocardiographique renforcée ; si besoin,
adaptation de la posologie de la méthadone pendant le traitement par la
cimétidine et après son arrêt.
Augmentation des concentrations plasmatiques de méthadone
avec surdosage et risque majoré d’allongement de l’intervalle QT et
de troubles du rythme ventriculaire, notamment de torsades de
pointes.
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique et électrocardiographique renforcée ; si besoin,
adaptation de la posologie de la méthadone pendant le traitement par la
fluvoxamine et après son arrêt.
Augmentation des concentrations plasmatiques de méthadone
avec surdosage et risque majoré d’allongement de l’intervalle QT et
de troubles du rythme ventriculaire, notamment de torsades de
pointes.
164
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Augmenter la fréquence des prises de méthadone (2 à 3 fois par jour au
lieu d'une fois par jour).
Diminution des concentrations plasmatiques de méthadone avec
risque d'apparition d'un syndrome de sevrage, par augmentation de
son métabolisme hépatique.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique régulière et adaptation éventuelle de la posologie
de méthadone.
Diminution des concentrations plasmatiques de méthadone avec
risque d'apparition d'un syndrome de sevrage par augmentation de
son métabolisme hépatique par le ritonavir.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations de méthadone par le millepertuis,
avec risque de syndrome de sevrage.
+ MORPHINIQUES AGONISTES-ANTAGONISTES
CONTRE-INDICATIONDiminution de l'effet de la méthadone par blocage compétitif des
récepteurs.
+ QUETIAPINE
A prendre en comptePossible augmentation des concentrations de méthadone, avec
signes de surdosage.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine
et la pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ VORICONAZOLE
Précaution d'emploi
Surveillance clinique et électrocardiographique renforcée ; si besoin,
adaptation de la posologie de la méthadone pendant le traitement par le
voriconazole et après son arrêt.
Augmentation des concentrations plasmatiques de méthadone
avec surdosage et risque majoré d’allongement de l’intervalle QT et
de troubles du rythme ventriculaire, notamment de torsades de
pointes.
METHENAMINE
+ SULFAMETHIZOL
Association DECONSEILLEEPrécipitation cristalline dans les voies urinaires (favorisée par
l'acidification des urines).
METHOTREXATE
Voir aussi : cytotoxiques - médicaments néphrotoxiques
+ ACIDE ACETYLSALICYLIQUE
CI - PE
Avec le méthotrexate utilisé à des doses > 20 mg/semaine :
- contre-indication avec l'acide acétylsalicylique utilisé à doses
antalgiques, antipyrétiques ou anti-inflammatoires
- précaution d'emploi avec des doses antiagrégantes plaquettaires
d'acide acétylsalicylique. Contrôle hebdomadaire de l’hémogramme
durant les premières semaines de l’association. Surveillance accrue en
cas d’altération (même légère) de la fonction rénale, ainsi que chez le
sujet âgé.
Avec le méthotrexate utilisé à des doses =< 20 mg/semaine :
- précaution d'emploi avec l'acide acétylsalicylique utilisé à doses
antalgiques, antipyrétiques ou anti-inflammatoires. Contrôle
hebdomadaire de l’hémogramme durant les premières semaines de
l’association. Surveillance accrue en cas d’altération (même légère) de
la fonction rénale, ainsi que chez le sujet âgé.
Majoration de la toxicité, notamment hématologique, du
méthotrexate (diminution de sa clairance rénale par l'acide
acétylsalicylique).
+ ACITRETINE
CONTRE-INDICATIONRisque de majoration de l'hépatotoxicité du méthotrexate.
165
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
ASDEC - PE
Association déconseillée:
- pour des doses de méthotrexate supérieures à 20 mg par semaine.
- avec le kétoprofène et le méthotrexate à des doses supérieures à 20
mg par semaines, respecter un intervalle d'au moins 12 heures entre
l'arrêt ou le début d'un traitement par kétoprofène et la prise de
méthotrexate.
Association nécessitant une précaution d'emploi :
- avec le méthotrexate utilisé à faibles doses (inférieures ou égales à 20
mg par semaine), contrôle hebdomadaire de l'hémogramme durant les
premières semaines de l'association. Surveillance accrue en cas
d'altération (même légère) de la fonction rénale, ainsi que chez le sujet
âgé.
Augmentation de la toxicité hématologique du méthotrexate
(diminution de la clairance rénale du méthotrexate par les anti-
inflammatoires).
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
ASDEC - APEC
Association déconseillée :
- avec le méthotrexate aux doses > 20 mg / semaine
A prendre en compte :
- pour des doses inférieures
Risque d’augmentation de la toxicité du méthotrexate par
diminution de son élimination.
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de ciclosporine et de
méthotrexate. Adaptation posologique si nécessaire pendant
l'association et après son arrêt.
Augmentation de la toxicité du méthotrexate et de la ciclosporine
avec augmentation de la créatininémie : diminution réciproque des
clairances des deux médicaments.
+ CIPROFLOXACINE
Association DECONSEILLEEAugmentation de la toxicité du méthotrexate par inhibition de sa
sécrétion tubulaire rénale par la ciprofloxacine.
+ PÉNICILLINES
Association DECONSEILLEEAugmentation des effets et de la toxicité hématologique du
méthotrexate : inhibition de la sécrétion tubulaire rénale du
méthotrexate par les pénicillines.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
méthotrexate par augmentation de son absorption intestinale par le
ponatinib.
+ PROBENECIDE
CONTRE-INDICATIONAugmentation de la toxicité du méthotrexate : inhibition de la
sécrétion tubulaire rénale du méthotrexate par le probénécide.
+ SULFAMIDES ANTIBACTÉRIENS
Précaution d'emploi
Dosage des concentrations de méthotrexate. Adapatation posologique
si nécessaire pendant l'association et après son arrêt.
Augmentation de la toxicité hématologique du méthotrexate.
+ TÉDIZOLIDE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
méthotrexate, par augmentation de son absorption avec le
tédizolide administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
+ TRIMETHOPRIME
CI - ASDEC
Contre-indication
- avec le méthotrexate utilisé à doses > 20 mg/semaine
Association déconseillée
- Avec le méthotrexate utilisé à des doses =< 20 mg/semaine
Augmentation de la toxicité hématologique du méthotrexate
(diminution de son excrétion rénale ainsi qu'inhibition de la
dihydrofolate réductase).
METHYLDOPA
Voir aussi : antihypertenseurs centraux - antihypertenseurs sauf alpha-bloquants - médicaments abaissant la pression artérielle - médicaments sédatifs
+ FER
Précaution d'emploi
Prendre les sels de fer à distance de la méthyldopa (plus de deux
heures, si possible).
Diminution de l'absorption digestive de la méthyldopa (formation de
complexes).
+ LEVODOPA
Précaution d'emploi
Surveillance clinique et éventuellement diminution des doses de
lévodopa.
Augmentation des effets de la lévodopa mais également de ses
effets indésirables. Majoration de l'effet antihypertenseur de la
méthyldopa.
166
+ LITHIUM
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de lithium.
Augmentation de la lithémie pouvant atteindre des valeurs
toxiques, avec signes de surdosage en lithium.
MÉTHYLERGOMÉTRINE
Voir aussi : alcaloïdes de l'ergot de seigle vasoconstricteurs
+ SULPROSTONE
CONTRE-INDICATION
Ne pas utiliser ces deux médicaments simultanément ou
successivement.
Risque de vasoconstriction coronaire pouvant être fatale.
METHYLPREDNISOLONE
Voir aussi : corticoïdes - corticoïdes métabolisés, notamment inhalés - glucocorticoïdes (sauf hydrocortisone) - hypokaliémiants - substances à absorption réduite par
les topiques gastro-intestinaux, antiacides et adsorbants
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle de l'INR 2 à 4 jours après le bolus de méthylprednisolone ou
en présence de tous signes hémorragiques.
Pour des doses de 0,5 à 1g de méthylprednisolone administrées en
bolus : augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ CICLOSPORINE
A prendre en compteAvec la méthylprednisolone administrée par voie IV : augmentation
possible des concentrations sanguines de ciclosporine et de la
créatininémie. Mécanisme invoqué : diminution de l'élimination
hépatique de la ciclosporine.
METOPROLOL
Voir aussi : antihypertenseurs sauf alpha-bloquants - bradycardisants - bêta-bloquants (sauf esmolol et sotalol) (y compris collyres) - bêta-bloquants (sauf esmolol) (y
compris collyres) - bêta-bloquants dans l'insuffisance cardiaque - médicaments abaissant la pression artérielle - substances à absorption réduite par les topiques
gastro-intestinaux, antiacides et adsorbants
+ ABIRATERONE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par l'abiratérone.
Chez l'insuffisant cardiaque, risque d'augmentation des effets
indésirables du métoprolol, par diminution de son métabolisme
hépatique par l'abiratérone.
+ BUPROPION
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par le bupropion.
Avec le métoprolol utilisé dans l'insuffisance cardiaque : risque
d'augmentation des effets indésirables du métoprolol par diminution
de son métabolisme hépatique par le bupropion.
+ CIMETIDINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par la cimétidine.
Avec le métoprolol utilisé dans l'insuffisance cardiaque, et la
cimétidine utilisée à des doses supérieures ou égales à 800 mg/j :
augmentation des concentrations du métoprolol, pouvant être
préjudiciables dans le cas du traitement de l'insuffisance cardiaque,
par diminution de son métabolisme hépatique par la cimétidine.
+ CINACALCET
Précaution d'emploi
Surveillance clinique et réduction de la posologie du métroprolol
pendant le traitement par cinacalcet.
Augmentation des concentrations plasmatiques de métroprolol
avec risque de surdosage, par diminution de son métabolisme
hépatique par le cinacalcet.
+ DARIFENACINE
Précaution d'emploi
Surveillance clinique et réduction de la posologie du métoprolol pendant
le traitement par darifénacine.
Augmentation des concentrations plasmatiques du métoprolol,
avec risque de surdosage, par diminution de son métabolisme
hépatique par la darifénacine.
+ DULOXETINE
Précaution d'emploi
Surveillance clinique et réduction de la posologie du métoprolol pendant
le traitement par la duloxétine et après son arrêt.
Augmentation des concentrations plasmatiques de métoprolol avec
risque de surdosage, par diminution de son métabolisme hépatique
par la duloxétine.
+ FLUOXETINE
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
métoprolol pendant la durée du traitement par la fluoxétine et après son
arrêt.
Risque de majoration des effets indésirables du métoprolol, avec
notamment bradycardie excessive, par inhibition de son
métabolisme par la fluoxétine.
+ MIRABÉGRON
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie du
métoprolol pendant l'association.
Avec le métoprolol utilisé dans l'insuffisance cardiaque,
augmentation des concentrations plasmatiques du métoprolol par
diminution de son métabolisme par le mirabégron.
167
+ PAROXETINE
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
métoprolol pendant la durée du traitement par la paroxétine et après
son arrêt.
Risque de majoration des effets indésirables du métoprolol, avec
notamment bradycardie excessive, par inhibition de son
métabolisme par la paroxétine.
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
A prendre en compteDiminution des concentrations plasmatiques du métoprolol avec
réduction de ses effets cliniques (augmentation de son
métabolisme hépatique).
+ RIFAMPICINE
A prendre en compteDiminution des concentrations plasmatiques et de l'efficacité du
bêta-bloquant (augmentation de son métabolisme hépatique).
+ ROLAPITANT
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par le rolapitant.
Chez l'insuffisant cardiaque, risque d'augmentation des effets
indésirables du métoprolol, par diminution de son métabolisme
hépatique par le rolapitant.
+ TERBINAFINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par la terbinafine.
Chez l'insuffisant cardiaque, risque d'augmentation des effets
indésirables du métoprolol, par diminution de son métabolisme
hépatique par la terbinafine.
METRONIDAZOLE
Voir aussi : antabuse (réaction)
+ BUSULFAN
Association DECONSEILLEEAvec le busulfan à fortes doses : doublement des concentrations
de busulfan par le métronidazole.
+ DISULFIRAME
Association DECONSEILLEERisque d’épisodes de psychose aiguë ou d’état confusionnel,
réversibles à l’arrêt de l’association.
+ FLUOROURACILE (ET, PAR EXTRAPOLATION, AUTRES FLUOROPYRIMIDINES)
A prendre en compteAugmentation de la toxicité du fluoro-uracile par diminution de sa
clairance.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
métronidazole pendant le traitement par l’inducteur et après son arrêt.
Diminution des concentrations plasmatiques du métronidazole par
augmentation de son métabolisme hépatique par l’inducteur.
+ LITHIUM
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Augmentation de la lithémie pouvant atteindre des valeurs
toxiques, avec signes de surdosage en lithium.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
métronidazole pendant le traitement par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques du métronidazole par
augmentation de son métabolisme hépatique par la rifampicine.
METYRAPONE
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Doubler la posologie de métyrapone.
Risque de faux négatif du test à la métyrapone, dû à une diminution
de ses concentrations plasmatiques, par augmentation de son
métabolisme hépatique par la phénytoïne.
MEXILETINE
Voir aussi : antiarythmiques
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
CONTRE-INDICATIONEffet inotrope négatif avec risque de décompensation cardiaque.
168
+ CAFEINE
A prendre en compteAugmentation des concentrations plasmatiques de caféine, par
inhibition de son métabolisme hépatique par la méxilétine.
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique et ECG. Adaptation de la posologie de la
méxilétine pendant le traitement par la fluvoxamine et après son arrêt.
Risque de majoration des effets indésirables de la méxilétine, par
inhibition de son métabolisme par la fluvoxamine.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique, ECG et éventuellement des concentrations
plasmatiques de la mexilétine ; s'il y a lieu, adaptation de la posologie
de la mexilétine pendant le traitement par la phénytoïne et après son
arrêt.
Diminution de l'activité antiarythmique, des concentrations
plasmatiques et de la demi-vie de la méxilétine (augmentation de
son métabolisme hépatique).
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par la mexilétine et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution du métabolisme hépatique de la théophylline).
MIANSERINE
Voir aussi : médicaments sédatifs
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEERisque d’inefficacité de la miansérine.
MICONAZOLE
+ ANTIVITAMINES K
CONTRE-INDICATIONHémorragies imprévisibles, éventuellement graves.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique étroite, dosage des concentrations plasmatiques
de phénytoïne et adaptation éventuelle de sa posologie pendant le
traitement par le miconazole et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
pouvant atteindre des valeurs toxiques, par inhibition du
métabolisme hépatique de la phénytoïne.
+ SULFAMIDES HYPOGLYCÉMIANTS
CONTRE-INDICATIONAugmentation de l'effet hypoglycémiant avec survenue possible de
manifestations hypoglycémiques, voire de coma.
MIDAZOLAM
Voir aussi : benzodiazépines et apparentés - médicaments sédatifs - substrats à risque du CYP3A4
+ DILTIAZEM
Précaution d'emploi
Surveillance clinique et réduction de la posologie pendant le traitement
par le diltiazem.
Augmentation des concentrations plasmatiques de midazolam par
diminution de son métabolisme hépatique, avec majoration de la
sédation.
+ FLUCONAZOLE
Précaution d'emploi
Surveillance clinique et réduction de la posologie de midazolam en cas
de traitement par le fluconazole.
Augmentation des concentrations plasmatiques de midazolam par
diminution de son métabolisme hépatique, avec majoration de la
sédation.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
A prendre en compteRisque de diminution des concentrations plasmatiques du
midazolam par l'anticonvulsivant.
+ INHIBITEURS PUISSANTS DU CYP3A4
ASDEC - PE
Association déconseillée:
- avec le midazolam per os
Précaution d'emploi avec :
- avec le midazolam IV et sublingual
Surveillance clinique et réduction de la posologie de midazolam en cas
de traitement par l'inhibiteur.
Augmentation des concentrations plasmatiques de midazolam par
diminution de son métabolisme hépatique, avec majoration de la
sédation.
169
+ MILLEPERTUIS
A prendre en compteRisque de diminution des concentrations plasmatiques de
midazolam par le millepertuis.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du midazolam par
diminution de son métabolisme hépatique par la bithérapie.
+ RIFAMPICINE
Association DECONSEILLEERisque d'absence d'effet du midazolam, avec diminution très
importante de ses concentrations plasmatiques, par augmentation
de son métabolisme hépatique.
+ ROXITHROMYCINE
A prendre en compteMajoration légère de la sédation.
+ STIRIPENTOL
Précaution d'emploi
Surveillance clinique et réduction de la posologie pendant le traitement
par le stiripentol.
Augmentation des concentrations plasmatiques du midazolam par
diminution de son métabolisme hépatique avec majoration de la
sédation.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique et réduction de la posologie de midazolam
pendant le traitement par le vérapamil.
Augmentation des concentrations plasmatiques de midazolam
(diminution de son métabolisme hépatique avec majoration de la
sédation).
MIDECAMYCINE
Voir aussi : macrolides (sauf spiramycine)
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
MIDODRINE
Voir aussi : bradycardisants - sympathomimétiques alpha (voies orale et/ou nasale)
+ DIGOXINE
Association DECONSEILLEE
Si cette association ne peut être évitée, renforcer la surveillance
clinique et ECG.
Troubles de l'automatisme (majoration de l'effet bradycardisant de
la midodrine) et troubles de la conduction auriculo-ventriculaire.
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONCrises hypertensives (inhibition du métabolisme des amines
pressives). Du fait de la durée d'action des IMAO, cette interaction
est encore possible 15 jours après l'arrêt de l'IMAO.
MIDOSTAURINE
+ INDUCTEURS ENZYMATIQUES
CONTRE-INDICATIONDiminution des concentrations de midostaurine par l’inducteur
enzymatique.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Augmentation des effets indésirables de la midostaurine par
l’inhibiteur.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations de midostaurine par le millepertuis.
MIFAMURTIDE
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
CONTRE-INDICATIONAux doses élevées d’AINS, risque de moindre efficacité du
mifamurtide.
170
+ CICLOSPORINE
CONTRE-INDICATIONRisque d'atteinte des macrophages spléniques et des cellules
phagocytaires mononuclées.
+ CORTICOÏDES
Association DECONSEILLEERisque de moindre efficacité du mifamurtide.
+ TACROLIMUS
CONTRE-INDICATIONRisque d'atteinte des macrophages spléniques et des cellules
phagocytaires mononuclées.
MILLEPERTUIS
Voir aussi : médicaments à l'origine d'un syndrome sérotoninergique
+ ANTICONVULSIVANTS MÉTABOLISÉS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques et de
l'efficacité de l'anticonvulsivant.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compteRisque d’inefficacité du traitement antisécrétoire par augmentation
de son métabolisme par le millepertuis.
+ ANTIVITAMINES K
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler l'INR avant puis après l'arrêt du millepertuis.
Diminution des concentrations plasmatiques de l'antivitamine K, en
raison de son effet inducteur enzymatique, avec risque de baisse
d'efficacité voire d'annulation de l'effet dont les conséquences
peuvent être éventuellement graves (évènement thrombotique).
+ BÉDAQUILINE
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
bédaquiline par augmentation de son métabolisme par l’inducteur.
+ BICTÉGRAVIR
CONTRE-INDICATIONDiminution très importante des concentrations de bictégravir, avec
risque de perte d’efficacité.
+ BUSPIRONE
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de la
buspirone par augmentation de son métabolisme par le millepertuis.
+ CANNABIDIOL
CONTRE-INDICATIONDiminution des concentrations plasmatiques de cannabidiol avec
risque de perte d’efficacité.
+ CARBAMAZEPINE
Association DECONSEILLEERisque de diminution des concentrations plasmatiques et de
l'efficacité de la carbamazepine.
+ CLOZAPINE
CONTRE-INDICATIONRisque d’inefficacité du traitement antipsychotique (diminution des
concentrations plasmatiques de clozapine par augmentation de son
métabolisme hépatique).
+ COBICISTAT
CONTRE-INDICATIONRisque de diminution de l’efficacité du cobicistat par augmentation
de son métabolisme par l’inducteur.
+ CYCLOPHOSPHAMIDE
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques du
métabolite actif du cyclophosphamide par le millepertuis, et donc
de sa toxicité.
171
+ CYPROTERONE
CONTRE-INDICATIONRisque de diminution de l'efficacité de la cyprotérone, par
augmentation de son métabolisme hépatique par le millepertuis.
+ DASABUVIR
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques du
dasabuvir par le millepertuis.
+ DIGOXINE
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler les concentrations plasmatiques (ou
l'efficacité) de la digoxine avant puis après l'arrêt du millepertuis.
Diminution de la digoxinémie, en raison de l'effet inducteur du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet, dont les conséquences peuvent être éventuellement graves
(décompensation d'une insuffisance cardiaque).
+ DOCETAXEL
CONTRE-INDICATIONRisque de moindre efficacité du taxane par augmentation de son
métabolisme par le millepertuis.
+ DOLUTÉGRAVIR
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
dolutégravir par augmentation de son métabolisme par le
millepertuis.
+ DRONEDARONE
Association DECONSEILLEEDiminution importante des concentrations de dronédarone par
augmentation de son métabolisme, sans modification notable du
métabolite actif.
+ EFAVIRENZ
CONTRE-INDICATIONRisque de diminution des concentrations d'éfavirenz, avec baisse
d'efficacité.
+ ESTROPROGESTATIFS CONTRACEPTIFS
CONTRE-INDICATIONDiminution des concentrations plasmatiques du contraceptif
hormonal, en raison de l'effet inducteur enzymatique du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet dont les conséquences peuvent être éventuellement graves
(survenue d'une grossesse).
+ ETOPOSIDE
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques d’étoposide
par le millepertuis.
+ FEXOFENADINE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la féxofénadine par
le millepertuis.
+ FOSTEMSAVIR
CONTRE-INDICATIONRisque de diminution significative des concentrations de
fostemsavir avec le millepertuis, avec réduction de la réponse
virologique.
+ GILTÉRITINIB
CONTRE-INDICATIONDiminution des concentrations plasmatiques de gilteritinib avec
risque de perte d’efficacité.
+ GLÉCAPRÉVIR + PIBRENTASVIR
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la bithérapie par
augmentation de son métabolisme par le millepertuis.
+ HORMONES THYROÏDIENNES
Association DECONSEILLEERisque de baisse de l’efficacité des hormones thyroïdiennes.
172
+ IDÉLALISIB
Association DECONSEILLEERisque de diminution importante des concentrations plasmatiques
d’idélalisib par augmentation de son métabolisme hépatique par le
millepertuis.
+ IMAO IRRÉVERSIBLES
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ IMMUNOSUPPRESSEURS
CONTRE-INDICATIONDiminution des concentrations sanguines de l'immunosuppresseur,
en raison de l'effet inducteur enzymatique du millepertuis, avec
risque de baisse d'efficacité voire d'annulation de l'effet dont les
conséquences peuvent être éventuellement graves (rejet de greffe).
+ INHIBITEURS DE LA 5-ALPHA REDUCTASE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de l’inhibiteur de la 5-
alpha réductase par le millepertuis.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler les concentrations plasmatiques (ou
l'efficacité) de l'inhibiteur de protéases avant puis après l'arrêt du
millepertuis.
Diminution des concentrations plasmatiques de l'inhibiteur de
protéases, en raison de l'effet inducteur enzymatique du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet dont les conséquences peuvent être éventuellement graves
(baisse de l'efficacité antirétrovirale).
+ INHIBITEURS DE TYROSINE KINASES MÉTABOLISÉS
CONTRE-INDICATIONDiminution des concentrations plasmatiques et de l’efficacité de
l’inhibiteur de tyrosine kinase, par augmentation de son
métabolisme par le millepertuis.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'apparition d'un syndrome sérotoninergique.
+ IRINOTECAN
CONTRE-INDICATIONDiminution des concentrations plasmatiques du métabolite actif de
l'irinotécan, avec risque d'échec du traitement cytotoxique.
+ ISAVUCONAZOLE
CONTRE-INDICATIONDiminution des concentrations plasmatiques d’isavuconazole par
augmentation de son métabolisme hépatique par le millepertuis.
+ ITRACONAZOLE
CONTRE-INDICATIONRisque de diminution importante des concentrations plasmatiques
d’itraconazole, avec risque de perte d’efficacité, par augmentation
de son métabolisme hépatique par le millepertuis.
+ IVABRADINE
Association DECONSEILLEERisque de diminution de l'efficacité de l’ivabradine, par
augmentation de son métabolisme par le millepertuis.
+ LÉDIPASVIR
CONTRE-INDICATIONRisque de diminution importante des concentrations plasmatiques
du lédipasvir par augmentation de son métabolisme hépatique par
le millepertuis.
+ LÉNACAPAVIR
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
173
+ LOMITAPIDE
Association DECONSEILLEERisque de diminution des concentrations plasmatiques du
lomitapide.
+ LURASIDONE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la lurasidone par
augmentation de son métabolisme hépatique par le millepertuis.
+ MACITENTAN
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
macitentan par augmentation de son métabolisme par le
millepertuis.
+ MARAVIROC
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
maraviroc pouvant conduire à une perte de la réponse virologique.
+ METHADONE
CONTRE-INDICATIONDiminution des concentrations de méthadone par le millepertuis,
avec risque de syndrome de sevrage.
+ MIDAZOLAM
A prendre en compteRisque de diminution des concentrations plasmatiques de
midazolam par le millepertuis.
+ MIDOSTAURINE
CONTRE-INDICATIONDiminution des concentrations de midostaurine par le millepertuis.
+ NEVIRAPINE
CONTRE-INDICATIONRisque de diminution significative des concentrations plasmatiques
de la névirapine par augmentation de son métabolisme hépatique
par le millepertuis.
+ NINTÉDANIB
Association DECONSEILLEEDiminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par le millepertuis.
+ OLAPARIB
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques d’olaparib et
de son efficacité, par augmentation de son métabolisme par le
millepertuis.
+ OXYCODONE
Association DECONSEILLEE
Adaptation éventuelle de la posologie de l’oxycodone .
Diminution des concentrations plasmatiques de l’oxycodone par
augmentation de son métabolisme par le millepertuis.
+ PACLITAXEL
CONTRE-INDICATIONRisque de moindre efficacité du taxane par augmentation de son
métabolisme par le millepertuis.
+ PROGESTATIFS CONTRACEPTIFS
CONTRE-INDICATIONDiminution des concentrations plasmatiques du contraceptif
hormonal, en raison de l'effet inducteur enzymatique du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet dont les conséquences peuvent être éventuellement graves
(survenue d'une grossesse).
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et ECG. S'il y a lieu, adaptation de la posologie de
la propafénone pendant l'association et après l'arrêt du millepertuis.
Diminution des concentrations plasmatiques de la propafénone par
augmentation de son métabolisme hépatique par le millepertuis.
174
+ QUETIAPINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
quétiapine par augmentation de son métabolisme hépatique par
l'inducteur, avec risque d’inefficacité.
+ RÉGORAFÉNIB
Association DECONSEILLEEDiminution des concentrations plasmatiques de régorafenib par
augmentation de son métabolisme par le millepertuis
+ RILPIVIRINE
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
rilpivirine par augmentation de son métabolisme hépatique par le
millepertuis.
+ ROLAPITANT
CONTRE-INDICATIONDiminution très importante des concentrations de rolapitant avec
risque de perte d’efficacité.
+ SIMVASTATINE
Association DECONSEILLEEDiminution de l’efficacité de l’hypocholestérolémiant par
augmentation de son métabolisme hépatique par le millepertuis.
+ SOFOSBUVIR
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
sofosbuvir par diminution de son absorption intestinale par
le millepertuis.
+ TAMOXIFENE
CONTRE-INDICATIONRisque d’inefficacité du tamoxifène par augmentation de son
métabolisme par le millepertuis.
+ TELITHROMYCINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de la télithromycine,
avec risque d'échec du traitement anti-infectieux, par augmentation
du métabolisme hépatique de la télithromycine par le millepertuis.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler les concentrations plasmatiques (ou
l'efficacité) du médicament associé avant puis après l'arrêt du
millepertuis.
Diminution des concentrations plasmatiques de la théophylline, en
raison de l'effet inducteur enzymatique du millepertuis, avec risque
de baisse d'efficacité voire d'annulation de l'effet dont les
conséquences peuvent être éventuellement graves (survenue d'un
trouble ventilatoire obstructif).
+ TICAGRELOR
CONTRE-INDICATIONRisque de diminution importante des concentrations plasmatiques
de ticagrelor par augmentation de son métabolisme hépatique par
le millepertuis, avec diminution de son effet thérapeutique.
+ ULIPRISTAL
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par l’inducteur.
+ VELPATASVIR
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par le
millepertuis, avec possible retentissement sur l’efficacité.
+ VÉNÉTOCLAX
CONTRE-INDICATIONDiminution importante des concentrations de vénétoclax, avec
risque de perte d’efficacité.
+ VERAPAMIL
CONTRE-INDICATIONRéduction importante des concentrations de vérapamil, avec risque
de perte de son effet thérapeutique.
175
+ VINCA-ALCALOÏDES CYTOTOXIQUES
CONTRE-INDICATIONRisque de moindre efficacité du cytotoxique par augmentation de
son métabolisme par le millepertuis.
+ VISMODÉGIB
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
vismodégib.
+ VORICONAZOLE
CONTRE-INDICATIONRéduction importante des concentrations de voriconazole, avec
risque de perte de son effet thérapeutique.
MINÉRALOCORTICOÏDES
(desoxycortone, fludrocortisone)
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie des
corticoïdes pendant le traitement par l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité des
corticoïdes par augmentation de leur métabolisme hépatique par
l'inducteur : les conséquences sont particulièrement importantes
chez les addisoniens traités par l'hydrocortisone et en cas de
transplantation.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie des
corticoïdes pendant le traitement par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité des
corticoïdes par augmentation de leur métabolisme hépatique par la
rifampicine ; les conséquences sont particulièrement importantes
chez les addisoniens traités par l'hydrocortisone et en cas de
transplantation.
MIRABÉGRON
+ METOPROLOL
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie du
métoprolol pendant l'association.
Avec le métoprolol utilisé dans l'insuffisance cardiaque,
augmentation des concentrations plasmatiques du métoprolol par
diminution de son métabolisme par le mirabégron.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
propafénone pendant l'association.
Augmentation des concentrations plasmatiques de la propafénone
par diminution de son métabolisme par le mirabégron.
MITOMYCINE C
Voir aussi : cytotoxiques
+ VINCA-ALCALOÏDES CYTOTOXIQUES
A prendre en compteRisque de majoration de la toxicité pulmonaire de la mitomycine et
des vinca-alcaloïdes.
MITOTANE
+ DASABUVIR
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques du
dasabuvir par le mitotane.
+ FOSTEMSAVIR
CONTRE-INDICATIONDiminution significative des concentrations de fostemsavir avec la
rifampicine, avec risque de réduction de la réponse virologique.
Éventualité non exclue avec le mitotane.
+ SPIRONOLACTONE
CONTRE-INDICATIONPossible réduction voire abolition de l'effet pharmacodynamique du
mitotane par la spironolactone, associé à une baisse des
concentrations du mitotane.
MOCLOBEMIDE
Voir aussi : IMAO-A réversibles, y compris oxazolidinones et bleu de méthylène - médicaments à l'origine d'un syndrome sérotoninergique
+ CIMETIDINE
Précaution d'emploi
Surveillance clinique avec adaptation éventuelle de la posologie de
moclobémide.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations du moclobémide, par
diminution de son métabolisme hépatique.
176
MODAFINIL
+ CICLOSPORINE
Association DECONSEILLEERisque de diminution des concentrations sanguines et de
l'efficacité de l'immunosuppresseur.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du modafinil.
Risque de diminution de l’efficacité contraceptive, pendant le
traitement et un cycle après l’arrêt du traitement par le modafinil, en
raison de son potentiel inducteur enzymatique.
MONTELUKAST
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de l'anti-
asthmatique pendant le traitement par l'inducteur et après son arrêt.
Risque de baisse de l'efficacité du montélukast par augmentation
de son métabolisme hépatique par l'inducteur.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
l'antiasthmatique pendant le traitement par la rifampicine et après son
arrêt.
Risque de baisse de l'efficacité du montélukast par augmentation
de son métabolisme hépatique par la rifampicine.
MORPHINE
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier III - morphiniques - médicaments sédatifs
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
morphine pendant le traitement par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
morphine et de son métabolite actif.
MORPHINIQUES
(alfentanil, buprenorphine, codeine, dextromethorphane, dihydrocodeine, ethylmorphine, fentanyl, hydromorphone, methadone, morphine, nalbuphine, nalméfène,
naloxone, naltrexone, noscapine, oxycodone, pethidine, pholcodine, remifentanil, sufentanil, tapentadol, tramadol)
+ BARBITURIQUES
A prendre en compteRisque majoré de sédation et de dépression respiratoire pouvant
entraîner coma et décès, notamment chez le sujet âgé. Il convient
de limiter autant que possible les doses et la durée de l’association.
+ BENZODIAZÉPINES ET APPARENTÉS
A prendre en compteRisque majoré de sédation et de dépression respiratoire pouvant
entraîner coma et décès, notamment chez le sujet âgé. Il convient
de limiter autant que possible les doses et la durée de l’association.
+ MÉDICAMENTS ATROPINIQUES
A prendre en compteRisque important d'akinésie colique, avec constipation sévère.
+ OXYBATE DE SODIUM
CONTRE-INDICATIONRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
MORPHINIQUES AGONISTES-ANTAGONISTES
(buprenorphine, nalbuphine)
+ ANALGÉSIQUES MORPHINIQUES DE PALIER II
Association DECONSEILLEEDiminution de l'effet antalgique par blocage compétitif des
récepteurs, avec risque d'apparition d'un syndrome de sevrage.
+ ANALGÉSIQUES MORPHINIQUES DE PALIER III
CONTRE-INDICATIONDiminution de l'effet antalgique par blocage compétitif des
récepteurs, avec risque d'apparition d'un syndrome de sevrage.
+ ANTITUSSIFS MORPHINIQUES VRAIS
Association DECONSEILLEEDiminution de l'effet antalgique ou antitussif du morphinique, par
blocage compétitif des récepteurs, avec risque d'apparition d'un
syndrome de sevrage.
177
+ METHADONE
CONTRE-INDICATIONDiminution de l'effet de la méthadone par blocage compétitif des
récepteurs.
+ MORPHINIQUES ANTAGONISTES PARTIELS
CONTRE-INDICATIONRisque de diminution de l’effet antalgique et/ou d’apparition d’un
syndrome de sevrage.
MORPHINIQUES ANTAGONISTES PARTIELS
(nalméfène, naltrexone)
+ ANALGÉSIQUES MORPHINIQUES DE PALIER II
Association DECONSEILLEERisque de diminution de l’effet antalgique.
+ ANALGÉSIQUES MORPHINIQUES DE PALIER III
CONTRE-INDICATIONRisque de diminution de l’effet antalgique.
+ MORPHINIQUES AGONISTES-ANTAGONISTES
CONTRE-INDICATIONRisque de diminution de l’effet antalgique et/ou d’apparition d’un
syndrome de sevrage.
+ MORPHINIQUES EN TRAITEMENT DE SUBSTITUTION
CONTRE-INDICATIONRisque d’apparition d’un syndrome de sevrage.
MORPHINIQUES EN TRAITEMENT DE SUBSTITUTION
(buprenorphine, methadone)
+ MORPHINIQUES ANTAGONISTES PARTIELS
CONTRE-INDICATIONRisque d’apparition d’un syndrome de sevrage.
MYCOPHENOLATE MOFETIL
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compteDiminution des concentrations de l’acide mycophénolique d’environ
un tiers, avec risque potentiel de baisse d’efficacité.
+ FLUOROQUINOLONES
A prendre en compteDiminution des concentrations de l’acide mycophénolique d’environ
un tiers, avec risque potentiel de baisse d’efficacité.
+ PÉNICILLINES A
A prendre en compteDiminution des concentrations de l’acide mycophénolique d’environ
un tiers, avec risque potentiel de baisse d’efficacité.
+ VACCINS VIVANTS ATTÉNUÉS
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
MYCOPHENOLATE SODIQUE
+ VACCINS VIVANTS ATTÉNUÉS
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
NALOXEGOL
+ DILTIAZEM
Précaution d'emploi
Adaptation posologique pendant l’association.
Augmentation des concentrations plasmatiques de naloxegol par le
diltiazem.
178
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations de naloxegol par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation très importante des concentrations du naloxegol par
l’inhibiteur.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEERisque d’augmentation des effets indésirables du naloxegol par le
pamplemousse.
+ VERAPAMIL
Précaution d'emploi
Adaptation posologique pendant l’association.
Augmentation des concentrations plasmatiques de naloxegol par le
vérapamil.
NEBIVOLOL
Voir aussi : antihypertenseurs sauf alpha-bloquants - bradycardisants - bêta-bloquants (sauf esmolol et sotalol) (y compris collyres) - bêta-bloquants (sauf esmolol) (y
compris collyres) - bêta-bloquants dans l'insuffisance cardiaque - médicaments abaissant la pression artérielle
+ FLUOXETINE
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
nébivolol pendant la durée du traitement par l’antidépresseur et après
son arrêt.
Risque de majoration des effets indésirables du nébivolol avec
notamment bradycardie excessive, par inhibition de son
métabolisme par l’antidépresseur.
+ PAROXETINE
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
nébivolol pendant la durée du traitement par l’antidépresseur et après
son arrêt.
Risque de majoration des effets indésirables du nébivolol avec
notamment bradycardie excessive, par inhibition de son
métabolisme par l’antidépresseur.
NÉTUPITANT
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution très importante des concentrations de nétupitant avec
risque de perte d'efficacité.
NEUROLEPTIQUES
(alimemazine, alizapride, amisulpride, aripiprazole, carpipramine, chlorpromazine, clozapine, cyamemazine, droperidol, flupentixol, fluphenazine, haloperidol,
levomepromazine, loxapine, metoclopramide, olanzapine, paliperidone, penfluridol, pimozide, pipamperone, pipotiazine, promethazine, propericiazine, quetiapine,
risperidone, sulpiride, tiapride, zuclopenthixol)
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
A prendre en compteEffet vasodilatateur et risque d'hypotension, notamment
orthostatique (effet additif).
+ LITHIUM
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d’apparition de signes neuropsychiques évocateurs d’un
syndrome malin des neuroleptiques ou d’une intoxication au lithium.
+ ORLISTAT
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
NEUROLEPTIQUES ANTIÉMÉTIQUES
(alizapride, metoclopramide)
+ DOPAMINERGIQUES
CONTRE-INDICATION
Utiliser un antiémétique dénué d'effets extrapyramidaux.
Antagonisme réciproque entre le dopaminergique et le
neuroleptique.
+ LEVODOPA
CONTRE-INDICATION
Utiliser un antiémétique dénué d'effets extrapyramidaux.
Antagonisme réciproque entre la lévodopa et le neuroleptique.
179
NEUROLEPTIQUES ANTIPSYCHOTIQUES (SAUF CLOZAPINE)
(amisulpride, aripiprazole, asenapine, chlorpromazine, cyamemazine, droperidol, flupentixol, fluphenazine, haloperidol, levomepromazine, loxapine, olanzapine,
paliperidone, penfluridol, pimozide, pipamperone, pipotiazine, propericiazine, quetiapine, risperidone, sulpiride, tiapride, zuclopenthixol)
+ ANTIPARKINSONIENS DOPAMINERGIQUES
Association DECONSEILLEEAntagonisme réciproque du dopaminergique et des neuroleptiques.
Le dopaminergique peut provoquer ou aggraver les troubles
psychotiques. En cas de nécessité d'un traitement par
neuroleptiques chez le patient parkinsonien traité par
dopaminergique, ces derniers doivent être diminués
progressivement jusqu'à l'arrêt (leur arrêt brutal expose à un risque
de "syndrome malin des neuroleptiques").
+ ARIPIPRAZOLE
A prendre en compteRisque de moindre efficacité, notamment de l’aripiprazole, suite à
l’antagonisme des récepteurs dopaminergiques par le
neuroleptique.
+ DOPAMINERGIQUES, HORS PARKINSON
CONTRE-INDICATIONAntagonisme réciproque de l'agoniste dopaminergique et des
neuroleptiques.
+ LEVODOPA
Association DECONSEILLEE
Chez le patient parkinsonien, utiliser les doses minimales efficaces de
chacun des deux médicaments.
Antagonisme réciproque de la lévodopa et des neuroleptiques.
NEUROLEPTIQUES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
(amisulpride, chlorpromazine, cyamemazine, droperidol, flupentixol, fluphenazine, haloperidol, levomepromazine, pimozide, pipamperone, pipotiazine, sulpiride,
tiapride, zuclopenthixol)
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
NEVIRAPINE
Voir aussi : inducteurs enzymatiques
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique.
+ ATAZANAVIR
Association DECONSEILLEE
Si l’association s’avère nécessaire, adaptation posologique de
l’atazanavir avec surveillance clinique et biologique régulière,
notamment en début d’association.
Risque de baisse de l’efficacité de l’atazanavir par augmentation de
son métabolisme hépatique.
+ FLUCONAZOLE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
névirapine.
Doublement des concentrations de névirapine avec risque
d'augmentation de ses effets indésirables.
+ FOSAMPRENAVIR
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'amprénavir.
+ KETOCONAZOLE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de névirapine par
diminution de son métabolisme hépatique par le kétoconazole,
d'une part, et diminution des concentrations plasmatiques du
kétoconazole par augmentation de son métabolisme hépatique par
la névirapine, d'autre part.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution significative des concentrations plasmatiques
de la névirapine par augmentation de son métabolisme hépatique
par le millepertuis.
180
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de la névirapine par
augmentation de son métabolisme hépatique par la rifampicine.
+ VORICONAZOLE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite et
adaptation éventuelle de la posologie du voriconazole pendant
l'association.
Risque de baisse de l'efficacité du voriconazole par augmentation
de son métabolisme hépatique par la névirapine.
NICARDIPINE
Voir aussi : antagonistes des canaux calciques - antihypertenseurs sauf alpha-bloquants - dihydropyridines - médicaments abaissant la pression artérielle
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de sa posologie pendant le
traitement et après l'arrêt.
Augmentation des concentrations sanguines de
l'immunodépresseur, par inhibition de son métabolisme.
NICORANDIL
Voir aussi : dérivés nitrés et apparentés - médicaments à l'origine d'une hypotension orthostatique
+ ACIDE ACETYLSALICYLIQUE
Association DECONSEILLEEMajoration du risque ulcérogène et hémorragique digestif.
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Association DECONSEILLEEMajoration du risque ulcérogène et hémorragique digestif.
NIFEDIPINE
Voir aussi : antagonistes des canaux calciques - antihypertenseurs sauf alpha-bloquants - dihydropyridines - médicaments abaissant la pression artérielle
+ CICLOSPORINE
Association DECONSEILLEE
Utiliser une autre dihydropyridine.
Risque d'addition d'effets indésirables à type de gingivopathies.
+ CIMETIDINE
Précaution d'emploi
Surveillance clinique accrue : adapter la posologie de la nifédipine
pendant le tratiement par la cimétidine et après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de l'effet hypotenseur de la nifédipine par
inhibition de son métabolisme hépatique par la cimétidine.
+ DILTIAZEM
CONTRE-INDICATIONAugmentation importantes des concentrations de nifédipine par
diminution de son métabolisme hépatique par le diltiazem, avec
risque d'hypotension sévère.
NIMODIPINE
Voir aussi : antagonistes des canaux calciques - antihypertenseurs sauf alpha-bloquants - dihydropyridines - médicaments abaissant la pression artérielle
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEE
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par l'inducteur et après
son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique par
l'inducteur.
+ RIFAMPICINE
Association DECONSEILLEE
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par la rifampicine et
après son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
A prendre en compteAvec la nimodipine par voie orale, et par extrapolation, par voie
injectable : risque de majoration de l'effet hypotenseur de la
nimodipine par augmentation de ses concentrations plasmatiques
(diminution de son métabolisme par l'acide valproïque).
NINTÉDANIB
+ AMIODARONE
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'amiodarone.
181
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique pendant l’association.
Diminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par la carbamazépine.
+ CICLOSPORINE
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par la ciclosporine.
+ ERYTHROMYCINE
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'érythromycine.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'inhibiteur de protéases
boosté par ritonavir.
+ ITRACONAZOLE
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par l'itraconazole.
+ KETOCONAZOLE
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par le kétoconazole.
+ MILLEPERTUIS
Association DECONSEILLEEDiminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par le millepertuis.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique pendant l’association.
Diminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par la phénytoïne ou la fosphénytoïne.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique pendant l’association.
Diminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par la rifampicine.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par le vérapamil.
NORFLOXACINE
Voir aussi : fluoroquinolones - médicaments abaissant le seuil épileptogène - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et
adsorbants
+ CAFEINE
A prendre en compteAugmentation des concentrations plasmatiques de caféine, par
diminution du métabolisme hépatique de la caféine.
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium à distance de la norfloxacine (plus de 2
heures, si possible).
Diminution de l'absorption digestive de la norflloxacine.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution du métabolisme de la théophylline).
182
NORTRIPTYLINE
+ BUPROPION
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
nortriptyline pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la nortriptyline
par diminution de son métabolisme hépatique par le bupropion.
NOSCAPINE
Voir aussi : antitussifs morphine-like - morphiniques - médicaments sédatifs
+ ANTIVITAMINES K
Association DECONSEILLEEAugmentation de l’effet de l’antivitamine K et du risque
hémorragique.
OLANZAPINE
Voir aussi : médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - neuroleptiques - neuroleptiques antipsychotiques (sauf clozapine)
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique de
l'olanzapine.
Risque de diminution des concentrations plasmatiques de
l'olanzapine et de son efficacité thérapeutique, par augmentation de
son métabolisme hépatique par la carbamazépine.
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de
l’olanzapine pendant le traitement par fluvoxamine.
Augmentation des concentrations de l’olanzapine, avec risque de
majoration des effets indésirables, par diminution de son
métabolisme hépatique par la fluvoxamine.
OLAPARIB
+ AMIODARONE
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg 2
fois par jour avec l’amiodarone.
Augmentation des concentrations plasmatiques d’olaparib par l'
amiodarone
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations de
l'olaparib, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ CYTOTOXIQUES
Association DECONSEILLEERisque de majoration de l’effet myélosuppresseur du cytotoxique
+ DILTIAZEM
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par le
diltiazem.
+ FLUCONAZOLE
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par le
fluconazole.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution, éventuellement très importante selon l’inducteur, des
concentrations plasmatiques de l’olaparib par augmentation de son
métabolisme hépatique par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 150 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par
l’inhibiteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques d’olaparib et
de son efficacité, par augmentation de son métabolisme par le
millepertuis.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEERisque d’augmentation des effets indésirables de l’olaparib.
183
+ VERAPAMIL
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par le
vérapamil.
OMBITASVIR + PARITAPRÉVIR
(ombitasvir, paritaprévir)
+ ACIDE FUSIDIQUE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'acide fusidique
par diminution de son métabolisme hépatique par la bithérapie.
+ ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'alcaloïde de
l'ergot de seigle vasoconstricteur par diminution de son
métabolisme hépatique par la bithérapie.
+ ALFUZOSINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'afuzosine par
diminution de son métabolisme hépatique par la bithérapie.
+ AMIODARONE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'amiodarone
par diminution de son métabolisme hépatique par la bithérapie.
+ ATORVASTATINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l'atorvastatine
par diminution de son métabolisme hépatique par la bithérapie.
+ COLCHICINE
CI - ASDEC
Contre-indication:
- chez les patients insuffisants rénaux et/ou hépatiques.
Association déconseillée
- chez les patients ayant une fonction rénale et hépatique normale. Si
l’association s'avère nécessaire, une réduction de la dose de colchicine
ou une interruption du traitement par la colchicine est recommandée.
Augmentation des concentrations plasmatiques de la colchicine par
diminution de son métabolisme hépatique par la bithérapie.
+ DISOPYRAMIDE
CONTRE-INDICATIONRisque d’augmentation des concentrations plasmatiques de
disopyramide et de ses effets indésirables.
+ ETHINYLESTRADIOL
CONTRE-INDICATIONAugmentation de l’hépatotoxicité.
+ EVEROLIMUS
Association DECONSEILLEE
Si l’association s’avère nécessaire, contrôle strict de la fonction rénale,
dosage des concentrations sanguines de l'immunosuppresseur et
adaptation éventuelle de la posologie.
En association avec le ritonavir : augmentation significative des
concentrations de l’immunosuppresseur avec risque de majoration
de sa toxicité par la bithérapie.
+ INDUCTEURS ENZYMATIQUES
CONTRE-INDICATIONDiminution des concentrations plasmatiques de la bithérapie par
augmentation de son métabolisme hépatique par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATION
Contre-indication:
- sauf avec le ritonavir.
Augmentation des concentrations plasmatiques de la bithérapie par
diminution de son métabolisme hépatique par l’inhibiteur.
+ MIDAZOLAM
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du midazolam par
diminution de son métabolisme hépatique par la bithérapie.
184
+ PIMOZIDE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du pimozide par
diminution de son métabolisme hépatique par la bithérapie.
+ QUETIAPINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la quétiapine
par diminution de son métabolisme hépatique par la bithérapie.
+ QUINIDINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la quinidine par
diminution de son métabolisme hépatique par la bithérapie.
+ SALMETEROL
CONTRE-INDICATIONRisque d’augmentation des concentrations de salmétérol.
+ SILDENAFIL
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du sildénafil par
diminution de son métabolisme hépatique par la bithérapie.
+ SIMVASTATINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la simvastatine
par diminution de son métabolisme hépatique par la bithérapie.
+ SIROLIMUS
Association DECONSEILLEE
Si l’association s’avère nécessaire, contrôle strict de la fonction rénale,
dosage des concentrations sanguines de l'immunosuppresseur et
adaptation éventuelle de la posologie.
En association avec le ritonavir : augmentation significative des
concentrations de l’immunosuppresseur avec risque de majoration
de sa toxicité par la bithérapie.
+ TACROLIMUS
Association DECONSEILLEE
Si l’association s’avère nécessaire, contrôle strict de la fonction rénale,
dosage des concentrations sanguines de l'immunosuppresseur et
adaptation éventuelle de la posologie.
En association avec le ritonavir : augmentation significative des
concentrations de l’immunosuppresseur avec risque de majoration
de sa toxicité par la bithérapie.
+ TICAGRELOR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du ticagrélor par
diminution de son métabolisme hépatique par la bithérapie.
OMEPRAZOLE
Voir aussi : antisécrétoires inhibiteurs de la pompe à protons
+ ANAGRELIDE
A prendre en compte
Préférer un autre inhibiteur de la pompe à protons.
Risque de moindre efficacité de l'anagrélide par augmentation de
son métabolisme par l'oméprazole.
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations de
l'oméprazole, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique, ECG et de la digoxinémie, particulièrement chez
le sujet âgé.
Augmentation modérée de la digoxinémie par majoration de son
absorption par l'oméprazole.
+ ESCITALOPRAM
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ TACROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines du tacrolimus, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après son arrêt.
Augmentation des concentrations sanguines du tacrolimus.
185
ONDANSETRON
Voir aussi : sétrons
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ TRAMADOL
A prendre en compteDiminution de l’intensité et de la durée de l’effet analgésique du
tramadol et risque de diminution de l’effet antiémétique de
l’ondansétron.
OR
+ INHIBITEURS DE L'ENZYME DE CONVERSION
A prendre en compteAvec les sels d'or administrés par voie IV : risque de réaction
«nitritoïde» à l’introduction de l’IEC (nausées, vomissements, effets
vasomoteurs à type de flush, hypotension, éventuellement
collapsus).
ORGANOPLATINES
(carboplatine, cisplatine, oxaliplatine)
+ AMINOSIDES
A prendre en compteAddition des effets néphrotoxiques et/ou ototoxiques, notamment
en cas d'insuffisance rénale préalable.
+ DIURÉTIQUES DE L'ANSE
A prendre en compteRisque d’addition des effets ototoxiques et/ou néphrotoxiques.
ORLISTAT
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et, si besoin, ECG.
Risque de diminution des concentrations plasmatiques de
l'amiodarone et de son métabolite actif.
+ ANTIDÉPRESSEURS IMIPRAMINIQUES
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par l'orlistat et après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ CICLOSPORINE
Association DECONSEILLEE
Prendre l'orlistat à distance de la ciclosporine (au moins 3 heures).
Contrôle renforcé des dosages sanguins de ciclosporine, notamment en
début d’association, et lors d’augmentation éventuelle de la posologie
de l’orlistat.
Diminution des concentrations sanguines de ciclosporine par
diminution de son absorption intestinale, avec risque de perte de
l'activité immunosuppressive.
+ HORMONES THYROÏDIENNES
A prendre en compteRisque de déséquilibre du traitement thyroïdien substitutif en cas
de traitement par orlistat.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ LITHIUM
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
186
+ NEUROLEPTIQUES
A prendre en compteRisque d'échec thérapeutique en cas de traitement concomitant par
orlistat.
+ VITAMINE D
A prendre en compteDiminution de l'absorption de la vitamine D.
ORNIDAZOLE
Voir aussi : antabuse (réaction)
+ FLUOROURACILE (ET, PAR EXTRAPOLATION, AUTRES FLUOROPYRIMIDINES)
A prendre en compteAugmentation de la toxicité du fluoro-uracile par diminution de sa
clairance.
OXCARBAZEPINE
Voir aussi : anticonvulsivants métabolisés - hyponatrémiants - inducteurs enzymatiques
+ ESTROGÈNES NON CONTRACEPTIFS
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant le traitement par l'oxcarbazépine et après
son arrêt.
Risque de diminution de l'efficacité du traitement hormonal, par
augmentation de son métabolisme hépatique par l'oxcarbazépine.
+ LAMOTRIGINE
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques, avec
adaptation de la posologie de la lamotrigine si besoin.
Diminution des concentrations de la lamotrigine avec risque de
moindre efficacité, par augmentation de son métabolisme
hépatique par l'oxcarbazépine.
+ LÉNACAPAVIR
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
+ PÉRAMPANEL
A prendre en compteDiminution de moitié des concentrations de pérampanel et légère
augmentation de celles de l’oxcarbazépine.
+ TOPIRAMATE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique du
topiramate pendant le traitement par l'oxcarbazépine et après son arrêt.
Risque de diminution des concentrations du topiramate avec risque
de moindre efficacité, par augmentation de son métabolisme
hépatique par l'oxcarbazépine.
+ VELPATASVIR
Association DECONSEILLEERisque de diminution des concentrations de velpatasvir/sofosbuvir,
avec possible retentissement sur l’efficacité.
OXPRENOLOL
+ ERGOTAMINE
Précaution d'emploi
Surveillance clinique renforcée, en particulier pendant les premières
semaines de l'association.
Ergotisme : quelques cas de spasme artériel avec ischémie des
extrémités ont été observés (addition d'effets vasculaires).
OXYBATE DE SODIUM
Voir aussi : médicaments sédatifs
+ BARBITURIQUES
CONTRE-INDICATIONRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
+ MORPHINIQUES
CONTRE-INDICATIONRisque majoré de dépression respiratoire, pouvant être fatale en
cas de surdosage.
187
OXYCODONE
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier III - morphiniques - médicaments sédatifs - substrats à risque du CYP3A4
+ FLUCONAZOLE
Association DECONSEILLEEMajoration des effets indésirables, notamment respiratoires, de
l’oxycodone par diminution de son métabolisme hépatique par le
fluconazole.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEE
Adaptation éventuelle de la posologie d’oxycodone .
Diminution des concentrations plasmatiques de l’oxycodone par
augmentation de son métabolisme par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Surveillance clinique et adaptation éventuelle de la posologie de
l’oxycodone pendant le traitement par l'inhibiteur et après son arrêt.
Majoration des effets indésirables, notamment respiratoires, de
l’oxycodone par diminution de son métabolisme par l'inhibiteur.
+ MILLEPERTUIS
Association DECONSEILLEE
Adaptation éventuelle de la posologie de l’oxycodone .
Diminution des concentrations plasmatiques de l’oxycodone par
augmentation de son métabolisme par le millepertuis.
OZANIMOD
+ BRADYCARDISANTS
Association DECONSEILLEE
Surveillance clinique et ECG pendant au moins 6 heures.
Potentialisation des effets bradycardisants pouvant avoir des
conséquences fatales. Les bêta-bloquants sont d’autant plus à
risque qu’ils empêchent les mécanismes de compensation
adrénergique.
+ CICLOSPORINE
Association DECONSEILLEERisque d’augmentation des effets indésirables de l’ozanimod.
+ CLOPIDOGREL
A prendre en compteRisque d’augmentation des concentrations des métabolites actifs
de l’onazimod.
+ ELTROMBOPAG
Association DECONSEILLEERisque d’augmentation des effets indésirables de l’ozanimod.
+ GEMFIBROZIL
A prendre en compteAugmentation des concentrations des métabolites actifs de
l’onazimod.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations des métabolites actifs de l’ozanimod
d’environ 60%.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations des métabolites actifs de l’ozanimod
d’environ 60%.
P A S SODIQUE
Voir aussi : dérivés de l'acide aminosalicylique (ASA)
+ TENOFOVIR ALAFÉNAMIDE
A prendre en compteDiminution des deux tiers de l’exposition du ténofovir avec une
formulation de PAS calcique.
+ TENOFOVIR DISOPROXIL
A prendre en compteDiminution des deux tiers de l’exposition du ténofovir avec une
formulation de PAS calcique.
188
PACLITAXEL
Voir aussi : cytotoxiques - substrats à risque du CYP3A4
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
paclitaxel.
Risque de majoration des effets indésirables du paclitaxel par
diminution de son métabolisme hépatique par l’amiodarone.
+ CLOPIDOGREL
A prendre en compteAugmentation des concentrations du paclitaxel par le clopidogrel,
avec risque de majoration des effets indésirables.
+ DEFERASIROX
Précaution d'emploi
Surveillance clinique et biologique étroite.
Risque d’augmentation des concentrations plasmatiques du
paclitaxel par inhibition de son métabolisme hépatique par le
deferasirox.
+ GEMFIBROZIL
Précaution d'emploi
Surveillance clinique et biologique étroite et adaptation de la posologie
du paclitaxel pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
paclitaxel par inhibition de son métabolisme hépatique par le
gemfibrozil.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations du cytotoxique par augmentation de
son métabolisme par l’inducteur, avec risque de moindre efficacité.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de moindre efficacité du taxane par augmentation de son
métabolisme par le millepertuis.
+ TRIMETHOPRIME
Précaution d'emploi
Surveillance clinique et biologique étroite et adaptation de la posologie
du paclitaxel pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
paclitaxel par inhibition de son métabolisme hépatique par le
triméthoprime.
PAMPLEMOUSSE (JUS ET FRUIT)
Le jus de pamplemousse peut augmenter la biodisponibilité de quelques médicaments, notamment certains immunosuppresseurs (ciclosporine, tacrolimus, sirolimus),
les dihydropyridines, certaines statines et le cisapride. Les conséquences cliniques de ces interactions sont variables et dépendent de nombreux facteurs comme la
susceptibilité individuelle du patient, la nature ainsi que la quantité de jus de pamplemousse consommé, la simultanéité des prises, qui agit comme un facteur
favorisant, et la marge thérapeutique du médicament associé. En conséquence, il est recommandé de déconseiller au patient la consommation de jus de
pamplemousse en cas de traitements par ces médicaments, surtout s’il s’agit de simvastatine, dont les concentrations peuvent être considérablement augmentées.
(anpu
+ ATORVASTATINE
A prendre en compteAugmentation des concentrations plasmatiques de l'hypolipémiant,
avec risque de survenue d'effets indésirables, notamment
musculaires.
+ AVANAFIL
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l'avanafil, avec
risque d’hypotension.
+ BUSPIRONE
A prendre en compteRisque de majoration des effets indésirables de la buspirone par
diminution de son métabolisme par le pamplemousse.
+ CARBAMAZEPINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de carbamazépine,
avec risque de surdosage, par inhibition de son métabolisme par le
pamplemousse.
+ DRONEDARONE
Association DECONSEILLEEAugmentation des concentrations de dronédarone par inhibition de
son métabolisme par le pamplemousse.
+ HALOFANTRINE
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
189
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEEAugmentation de la biodisponibilité de l’immunosuppresseur et par
conséquent de ses effets indésirables.
+ IVABRADINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de l’ivabradine et
de ses effets indésirables (inhibition de son métabolisme intestinal
par le pamplemousse).
+ IVACAFTOR (SEUL OU ASSOCIÉ)
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques
d’ivacaftor par le jus de pamplemousse.
+ LERCANIDIPINE
A prendre en compteRisque majoré d'effets indésirables, notamment d'oedèmes, par
diminution du métabolisme intestinal de la dihydropyridine.
+ LURASIDONE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la lurasidone
par diminution de son métabolisme par le pamplemousse.
+ NALOXEGOL
Association DECONSEILLEERisque d’augmentation des effets indésirables du naloxegol par le
pamplemousse.
+ OLAPARIB
Association DECONSEILLEERisque d’augmentation des effets indésirables de l’olaparib.
+ RÉGORAFÉNIB
Association DECONSEILLEEAugmentation des concentrations plasmatiques de régorafenib par
diminution de son métabolisme hépatique par le pamplemousse.
+ SERTRALINE
Association DECONSEILLEEAugmentation parfois importante des concentrations de
l’antidépresseur chez certains patients par diminution de son
métabolisme intestinal.
+ SIMVASTATINE
Association DECONSEILLEEAugmentation considérable des concentrations plasmatiques de
l'hypolipémiant, avec risque de survenue d'effets indésirables,
notamment musculaires.
+ TICAGRELOR
Association DECONSEILLEEDoublement des concentrations plasmatiques de l'antiagrégant,
avec risque de majoration des effets indésirables, notamment
hémorragiques.
+ TOLVAPTAN
Association DECONSEILLEEAugmentation importante (entre 2 à 5 fois en moyenne) des
concentrations de tolvaptan, avec risque de majoration importante
des effets indésirables, notamment diurèse importante,
déshydratation, insuffisance rénale aiguë.
+ VARDENAFIL
Association DECONSEILLEEAugmentation des concentrations plasmatiques du vardénafil, avec
risque d’hypotension.
+ VÉNÉTOCLAX
Association DECONSEILLEEAugmentation des concentrations de vénétoclax, avec risque de
majoration des effets indésirables.
+ VERAPAMIL
A prendre en compteAugmentation des concentrations plasmatiques de vérapamil, avec
risque de survenue d’effets indésirables.
190
PANOBINOSTAT
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et ECG. Débuter le traitement à dose réduite de
moitié (10 mg).
Risque de majoration des effets indésirables, notamment
cardiaques, du panobinostat par diminution de son métabolisme
par l’inhibiteur.
PARACETAMOL
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par le paracétamol et après
son arrêt.
Risque d’augmentation de l’effet de l’antivitamine K et du risque
hémorragique en cas de prise de paracétamol aux doses
maximales (4 g/j) pendant au moins 4 jours.
+ FLUCLOXACILLINE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance étroite avec mesure de
la 5-oxoproline urinaire.
Risque accru d'acidose métabolique à trou anionique élevé,
notamment en cas d'insuffisance rénale sévère, de sepsis, de
facteurs prédisposant à la déplétion en glutathion (malnutrition,
alcoolisme chronique…), ainsi qu’en cas d’utilisation de
paracétamol aux doses quotidiennes maximales.
PAROXETINE
Voir aussi : hyponatrémiants - inhibiteurs sélectifs de la recapture de la sérotonine - médicaments abaissant le seuil épileptogène - médicaments à l'origine d'un
syndrome sérotoninergique
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
carbamazépine et réduction éventuelle de la posologie de la
carbamazépine pendant le traitement par l'antidépresseur
sérotoninergique et après son arrêt.
Augmentation des concentrations plasmatiques de carbamazépine
avec signes de surdosage.
+ CODEINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ MEQUITAZINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
métoprolol pendant la durée du traitement par la paroxétine et après
son arrêt.
Risque de majoration des effets indésirables du métoprolol, avec
notamment bradycardie excessive, par inhibition de son
métabolisme par la paroxétine.
+ NEBIVOLOL
Précaution d'emploi
Surveillance clinique accrue ; si besoin, adaptation de la posologie du
nébivolol pendant la durée du traitement par l’antidépresseur et après
son arrêt.
Risque de majoration des effets indésirables du nébivolol avec
notamment bradycardie excessive, par inhibition de son
métabolisme par l’antidépresseur.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ RISPERIDONE
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique de la
rispéridone.
Augmentation de la fraction active de la rispéridone par diminution
de son métabolisme hépatique par la paroxétine, avec risque de
majoration des effets indésirables.
+ TAMOXIFENE
Association DECONSEILLEEBaisse de l’efficacité du tamoxifène, par inhibition de la formation
de son métabolite actif par la paroxétine.
+ TETRABENAZINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ TRAMADOL
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
191
PEFLOXACINE
Voir aussi : fluoroquinolones - médicaments abaissant le seuil épileptogène - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et
adsorbants
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution du métabolisme de la théophylline).
PEG-INTERFERON ALFA-2A
+ TELBIVUDINE
CONTRE-INDICATIONRisque majoré de neuropathies périphériques.
PEMETREXED
Voir aussi : cytotoxiques
+ ACIDE ACETYLSALICYLIQUE
ASDEC - PE
Association déconseillée :
- en cas de fonction rénale faible à modérée .
Précaution d'emploi :
- en cas de fonction rénale normale. Surveillance biologique de la
fonction rénale.
Risque de majoration de la toxicité du pemetrexed (diminution de
sa clairance rénale par l’acide acétylsalicylique à doses anti-
inflammatoires).
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
ASDEC - PE
Association déconseillée :
- en cas de fonction rénale faible à modérée.
Précaution d'emploi :
- en cas de fonction rénale normale. Surveillance biologique de la
fonction rénale.
Risque de majoration de la toxicité du pemetrexed (diminution de
sa clairance rénale par les AINS).
PÉNEMS
(ertapenem, imipenem, meropenem)
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Association DECONSEILLEERisque de survenue de crises convulsives, par diminution rapide
des concentrations plasmatiques de l’acide valproïque, pouvant
devenir indétectables.
PENICILLAMINE
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ FER
Précaution d'emploi
Prendre les sels de fer à distance de la pénicillamine (plus de 2 heures,
si possible).
Diminution de l'absorption digestive de la pénicillamine.
PÉNICILLINES
(amoxicilline, ampicilline, benethamine-penicilline, benzylpenicilline, cloxacilline, flucloxacilline, oxacilline, phenoxymethylpenicilline, piperacilline, pivmécillinam,
témocilline, ticarcilline)
+ METHOTREXATE
Association DECONSEILLEEAugmentation des effets et de la toxicité hématologique du
méthotrexate : inhibition de la sécrétion tubulaire rénale du
méthotrexate par les pénicillines.
PÉNICILLINES A
(amoxicilline, ampicilline, ticarcilline)
+ ALLOPURINOL
A prendre en compteRisque accru de réactions cutanées.
+ MYCOPHENOLATE MOFETIL
A prendre en compteDiminution des concentrations de l’acide mycophénolique d’environ
un tiers, avec risque potentiel de baisse d’efficacité.
192
PENTAMIDINE
Voir aussi : antiparasitaires susceptibles de donner des torsades de pointes - médicaments néphrotoxiques - substances susceptibles de donner des torsades de
pointes
+ DIDANOSINE
Précaution d'emploi
Surveillance de l'amylasémie. Ne pas associer si l'amylasémie est à la
limite supérieure de la normale.
Risque majoré de survenue de pancréatite par addition d'effets
indésirables.
+ FOSCARNET
Précaution d'emploi
Surveillance de la calcémie et supplémentation si nécessaire.
Risque d'hypocalcémie sévère.
+ STAVUDINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
PENTOSTATINE
Voir aussi : cytotoxiques
+ CYCLOPHOSPHAMIDE
Association DECONSEILLEEMajoration du risque de toxicité pulmonaire pouvant être fatale.
+ FLUDARABINE
Association DECONSEILLEEMajoration du risque de toxicité pulmonaire pouvant être fatale.
PENTOXIFYLLINE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la pentoxifylline et 8 jours
après son arrêt.
Augmentation du risque hémorragique.
+ COBIMÉTINIB
Précaution d'emploi
Surveillance clinique.
Augmentation du risque hémorragique.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par la pentoxifylline et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(compétition au niveau du métabolisme hépatique de la
théophylline).
PÉRAMPANEL
Voir aussi : anticonvulsivants métabolisés - médicaments sédatifs
+ CYPROTERONE
Association DECONSEILLEE
Dans son utilisation comme contraceptif hormonal: utiliser de
préférence une autre méthode de contraception en particulier de type
mécanique, pendant la durée de l'association et un cycle suivant.
Pour des doses de pérampanel > ou = à 12 mg/jour, risque de
diminution de l'efficacité de la cyprotérone.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
A prendre en compteDiminution importante (jusqu’aux deux-tiers) des concentrations de
pérampanel.
+ OXCARBAZEPINE
A prendre en compteDiminution de moitié des concentrations de pérampanel et légère
augmentation de celles de l’oxcarbazépine.
+ PROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique.
Pour des doses de pérampanel >= 12 mg/jour : Risque de
diminution de l’efficacité contraceptive.
193
+ RIFAMPICINE
A prendre en compteDiminution importante (jusqu’aux deux-tiers) des concentrations de
pérampanel.
PETHIDINE
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier III - morphiniques - médicaments sédatifs - médicaments à l'origine d'un
syndrome sérotoninergique
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ IMAO-B
CONTRE-INDICATIONManifestations d'excitation centrale évoquant un syndrome
sérotoninergique : diarrhée, tachycardie, sueurs, tremblements,
confusion voire coma.
PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
(phenobarbital, primidone)
+ ACIDE CHOLIQUE
CONTRE-INDICATIONEffet antagoniste du barbiturique.
+ CARBAMAZEPINE
A prendre en compte
Prudence quant à l'interprétation des concentrations plasmatiques.
Diminution progressive des concentrations plasmatiques de
carbamazépine et de son métabolite actif sans modification
apparente de l'efficacité anticomitiale.
+ FELBAMATE
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénobarbital avec adaptation de la posologie si besoin.
Diminution des concentrations plasmatiques et de l'efficacité du
felbamate et augmentation des concentrations plasmatiques du
phénobarbital, avec risque de surdosage.
+ FOLATES
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques, et
adaptation, s'il y a lieu, de la posologie du phénobarbital pendant la
supplémentation folique et après son arrêt.
Diminution des concentrations plasmatiques du phénobarbital, par
augmentation de son métabolisme dont les folates représentent un
des cofacteurs.
+ IFOSFAMIDE
Association DECONSEILLEERisque de majoration de la neurotoxicité de l'ifosfamide par
augmentation de son métabolisme hépatique par le phénobarbital.
+ METOPROLOL
A prendre en compteDiminution des concentrations plasmatiques du métoprolol avec
réduction de ses effets cliniques (augmentation de son
métabolisme hépatique).
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
A prendre en compteEn cas de traitement antérieur par le phénobarbital ou la primidone,
et adjonction de phénytoïne, augmentation des concentrations
plasmatiques de phénobarbital pouvant entraîner des signes
toxiques (inhibition du métabolisme par compétition).
En cas de traitement antérieur par la phénytoïne et adjonction de
phénobarbital ou de primidone, variations imprévisibles :
- les concentrations plasmatiques de phénytoïne sont le plus
souvent diminuées (augmentation du métabolisme) sans que cette
diminution affecte défavorablement l'activité anticonvulsivante. A
l'arrêt du phénobarbital ou de la primidone, possibilité d'effets
toxiques de la phénytoïne
- il peut arriver que les concentrations de phénytoïne soient
augmentées (inhibition du métabolisme par compétition).
+ PROPRANOLOL
A prendre en compteDiminution des concentrations plasmatiques du propranolol avec
réduction de ses effets cliniques (augmentation de son
métabolisme hépatique).
194
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
(fosphenytoine, phenytoine)
+ AMIODARONE
Association DECONSEILLEEMajoration du risque de troubles du rythme ventriculaire par
potentialisation des effets antiarythmiques, ainsi que des effets
indésirables neurologiques, par diminution du métabolisme
hépatique de la phénytoïne par l’amiodarone.
+ CARBAMAZEPINE
A prendre en compte
Prudence dans l'interprétation des concentrations plasmatiques.
Réduction réciproque des concentrations plasmatiques
(augmentation du métabolisme sans modification apparente de
l'efficacité anticomitiale).
+ CIMETIDINE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite, dosage
des concentrations plasmatiques de phénytoïne et adaptation
éventuelle de sa posologie pendant le traitement par la cimétidine et
après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation des concentrations plasmatiques de
phénytoïne avec possibilité d'apparition des signes habituels de
surdosage.
+ CIPROFLOXACINE
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
l’anticonvulsivant pendant le traitement par ciprofloxacine et après son
arrêt.
Variation, éventuellement importante, des concentrations de
phénytoïne en cas de traitement par la ciprofloxacine.
+ CLOPIDOGREL
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage (inhibition du métabolisme de la
+ CYTOTOXIQUES
Association DECONSEILLEERisque de survenue de convulsions par diminution de l'absorption
digestive de la seule phénytoïne par le cytotoxique, ou bien risque
de majoration de la toxicité ou de perte d'efficacité du cytotoxique
par augmentation de son métabolisme hépatique par la phénytoïne
ou la fosphénytoïne.
+ DIAZEPAM
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne.
Variations imprévisibles : les concentrations plasmatiques de
phénytoïne peuvent augmenter, avec signes de surdosage, mais
aussi diminuer ou rester stables.
+ DISULFIRAME
Association DECONSEILLEE
Si elle ne peut être évitée, contrôle clinique et des concentrations
plasmatiques de phénytoïne pendant le traitement par le disulfirame et
après son arrêt.
Augmentation importante et rapide des concentrations
plasmatiques de phénytoïne avec signes toxiques (inhibition de son
métabolisme).
+ FELBAMATE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques de
phénytoïne et si besoin, adaptation de sa posologie pendant le
traitement par le felbamate.
Augmentation des concentrations plasmatiques de phénytoïne
avec risque de surdosage, par inhibition de son métabolisme par le
felbamate.
+ FLUCONAZOLE
Précaution d'emploi
Surveillance clinique et biologique étroite.
Augmentation des concentrations plasmatiques de phénytoïne
pouvant atteindre des valeurs toxiques. Mécanisme invoqué :
inhibition du métabolisme hépatique de la phénytoïne.
+ FLUOXETINE
Précaution d'emploi
Surveillance clinique et éventuellement contrôle des concentrations
plasmatiques de phénytoïne. Si besoin, adaptation posologique pendant
le traitement par la fluoxétine et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage, par inhibition du métabolisme de la
phénytoïne.
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique et éventuellement contröle des concentrations
plamatiques de phénytoïne. Si besoin, adaptation posologique de la
phénytoïne pendant le traitement par la fluvoxamine et après son arrët.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage, par inhibition du métabolisme hépatique
de la phénytoïne.
195
+ FOLATES
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne. Adaptation éventuelle de la posologie de la phénytoïne
pendant la supplémentation folique et après son arrêt.
Diminution des concentrations plasmatiques de phénytoïne par
augmentation de son métabolisme dont les folates représentent un
des cofacteurs.
+ FUROSEMIDE
Précaution d'emploi
Utiliser éventuellement des doses plus élevées de furosémide.
Diminution de l'effet diurétique pouvant atteindre 50 %.
+ ISONIAZIDE
Précaution d'emploi
Surveillance clinique étroite, dosage des concentrations plasmatiques
de phénytoïne et adaptation éventuelle de sa posologie pendant le
traitement par l'isoniazide et après son arrêt.
Surdosage en phénytoïne (diminution de son métabolisme).
+ METYRAPONE
Précaution d'emploi
Doubler la posologie de métyrapone.
Risque de faux négatif du test à la métyrapone, dû à une diminution
de ses concentrations plasmatiques, par augmentation de son
métabolisme hépatique par la phénytoïne.
+ MEXILETINE
Précaution d'emploi
Surveillance clinique, ECG et éventuellement des concentrations
plasmatiques de la mexilétine ; s'il y a lieu, adaptation de la posologie
de la mexilétine pendant le traitement par la phénytoïne et après son
arrêt.
Diminution de l'activité antiarythmique, des concentrations
plasmatiques et de la demi-vie de la méxilétine (augmentation de
son métabolisme hépatique).
+ MICONAZOLE
Précaution d'emploi
Surveillance clinique étroite, dosage des concentrations plasmatiques
de phénytoïne et adaptation éventuelle de sa posologie pendant le
traitement par le miconazole et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
pouvant atteindre des valeurs toxiques, par inhibition du
métabolisme hépatique de la phénytoïne.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Diminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par la phénytoïne ou la fosphénytoïne.
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
A prendre en compteEn cas de traitement antérieur par le phénobarbital ou la primidone,
et adjonction de phénytoïne, augmentation des concentrations
plasmatiques de phénobarbital pouvant entraîner des signes
toxiques (inhibition du métabolisme par compétition).
En cas de traitement antérieur par la phénytoïne et adjonction de
phénobarbital ou de primidone, variations imprévisibles :
- les concentrations plasmatiques de phénytoïne sont le plus
souvent diminuées (augmentation du métabolisme) sans que cette
diminution affecte défavorablement l'activité anticonvulsivante. A
l'arrêt du phénobarbital ou de la primidone, possibilité d'effets
toxiques de la phénytoïne
- il peut arriver que les concentrations de phénytoïne soient
augmentées (inhibition du métabolisme par compétition).
+ SUCRALFATE
Précaution d'emploi
Prendre le sucralfate à distance de la phénytoïne (plus de 2 heures, si
possible).
Diminution de l'absorption digestive de la phénytoïne.
+ SULFAFURAZOL
Association DECONSEILLEE
Utiliser de préférence une autre classe d'anti-infectieux, sinon
surveillance clinique étroite, dosage des concentrations de phénytoïne
et adaptation éventuelle de sa posologie pendant le traitement par le
sulfamide anti-infectieux et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
jusqu'à des valeurs toxiques (inhibition de son métabolisme).
+ SULFAMETHIZOL
Association DECONSEILLEE
Utiliser de préférence une autre classe d'anti-infectieux, sinon
surveillance clinique étroite, dosage des concentrations de phénytoïne
et adaptation éventuelle de sa posologie pendant le traitement par le
sulfamide anti-infectieux et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
jusqu'à des valeurs toxiques (inhibition de son métabolisme).
+ SULFAMETHOXAZOLE
Association DECONSEILLEE
Utiliser de préférence une autre classe d'anti-infectieux, sinon
surveillance clinique étroite, dosage des concentrations de phénytoïne
et adaptation éventuelle de sa posologie pendant le traitement par le
sulfamide anti-infectieux et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
jusqu'à des valeurs toxiques (inhibition de son métabolisme).
196
+ TICLOPIDINE
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage (inhibition du métabolisme de la
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
PILOCARPINE
Voir aussi : bradycardisants
+ ANTICHOLINESTÉRASIQUES
A prendre en compteRisque d'addition des effets indésirables cholinergiques,
notamment digestifs.
PIMOZIDE
Voir aussi : médicaments abaissant le seuil épileptogène - médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - neuroleptiques -
neuroleptiques antipsychotiques (sauf clozapine) - neuroleptiques susceptibles de donner des torsades de pointes - substances susceptibles de donner des torsades
de pointes - substrats à risque du CYP3A4
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations du
pimozide, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ APREPITANT
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ DALFOPRISTINE
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ DILTIAZEM
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ EFAVIRENZ
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ FLUCONAZOLE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ FLUOXETINE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ JOSAMYCINE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ LÉTERMOVIR
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
197
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du pimozide par
diminution de son métabolisme hépatique par la bithérapie.
+ PAROXETINE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ QUINUPRISTINE
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SERTRALINE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ STIRIPENTOL
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ TRICLABENDAZOLE
CONTRE-INDICATION
Respecter un délai de 24 heures entre l’arrêt du triclabendazole et la
prise du médicament torsadogène, et inversement.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes (inhibition du métabolisme hépatique du
médicament torsadogène).
+ VERAPAMIL
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaires, notamment, de
torsades de pointes.
PIPÉRACILLINE/TAZOBACTAM
(pipéracilline, tazobactam)
+ VANCOMYCINE
Association DECONSEILLEEMajoration de la néphrotoxicité par comparaison à la vancomycine
seule.
PIRFENIDONE
+ FLUVOXAMINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de pirfenidone
avec signes de surdosage.
PITAVASTATINE
Voir aussi : inhibiteurs de l'HMG-CoA réductase (statines) - médicaments à l'origine d'atteintes musculaires
+ CICLOSPORINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, ou de néphrotoxicité, par diminution du
métabolisme de la pitavastatine.
POLYMYXINE B
+ AMINOSIDES
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance stricte avec une
justification bactériologique indiscutable.
Addition des effets néphrotoxiques.
+ CURARES
Précaution d'emploi
Surveiller le degré de curarisation en fin d'anesthésie.
Potentialisation des curares lorque l'antibiotique est administré par
voie parentérale et/ou péritonéale avant, pendant ou après l'agent
curarisant.
198
POLYSTYRÈNE SULFONATE DE CALCIUM
Voir aussi : résines chélatrices
+ SORBITOL
CONTRE-INDICATIONPar voie orale ou rectale du sorbitol ou de la résine, et pour une
dose de sorbitol par prise >= 2,5 g chez l'enfant et 5 g chez l'adulte :
Risque de nécrose colique, éventuellement fatale.
+ TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ADSORBANTS
Précaution d'emploi
Comme avec tout médicament oral pris avec l’un ou l’autre de ces
médicaments, respecter un intervalle entre les prises (plus de 2 heures,
si possible).
Risque d'alcalose métabolique chez l'insuffisant rénal
POLYSTYRÈNE SULFONATE DE SODIUM
Voir aussi : résines chélatrices
+ SORBITOL
CONTRE-INDICATIONPar voie orale ou rectale du sorbitol ou de la résine, et pour une
dose de sorbitol par prise >= 2,5 g chez l'enfant et 5 g chez l'adulte :
Risque de nécrose colique, éventuellement fatale.
+ TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ADSORBANTS
Précaution d'emploi
Comme avec tout médicament oral pris avec l’un ou l’autre de ces
médicaments, respecter un intervalle entre les prises (plus de 2 heures,
si possible).
Risque d'alcalose métabolique chez l'insuffisant rénal.
PONATINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés - substrats à risque du CYP3A4
+ ATORVASTATINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de
l'atrovastatine par augmentation de son absorption intestinale par
le ponatinib.
+ COLCHICINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
colchicine par augmentation de son absorption intestinale par le
ponatinib.
+ DABIGATRAN
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
dabigatran par augmentation de son absorption intestinale par le
ponatinib.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
digoxine par augmentation de son absorption intestinale par le
ponatinib.
+ METHOTREXATE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
méthotrexate par augmentation de son absorption intestinale par le
ponatinib.
+ PRAVASTATINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
pravastatine par augmentation de son absorption intestinale par le
ponatinib.
+ ROSUVASTATINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
rosuvastatine par augmentation de son absorption intestinale par le
ponatinib.
+ SIMVASTATINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
simvastatine par augmentation de son absorption intestinale par le
ponatinib.
+ SULFASALAZINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
sulfasalazine par augmentation de son absorption intestinale par le
ponatinib.
199
PONÉSIMOD
+ BRADYCARDISANTS
Association DECONSEILLEE
Surveillance clinique et ECG continu pendant les 4 heures suivant la
première dose, jusqu'au lendemain si nécessaire.
Potentialisation des effets bradycardisants pouvant avoir des
conséquences fatales. Les bêta-bloquants sont d’autant plus à
risque qu’ils empêchent les mécanismes de compensation
adrénergique.
POSACONAZOLE
Voir aussi : inhibiteurs puissants du CYP3A4
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
Association DECONSEILLEE
Association déconseillée:
- uniquement avec la forme suspension buvable de posaconazole.
Diminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
Association DECONSEILLEE
Association déconseillée:
- uniquement avec la forme suspension buvable de posaconazole.
Diminution de l'absorption de l'azolé antifongique, par augmentation
du pH intragastrique par l'antisécrétoire.
+ ATAZANAVIR
A prendre en compteAugmentation des concentrations plasmatiques de l'atazanavir et
du risque d'hyperbilirubinémie.
+ ATORVASTATINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de
l’inhibiteur de l’HMG-CoA reductase).
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et, s'il y a lieu, de l'ECG et de la digoxinémie, avec
adaptation de la posologie de la digoxine pendant le traitement par le
posaconazole et après son arrêt.
Augmentation de la digoxinémie avec nausées, vomissements,
troubles du rythme.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique. Si possible, dosages plasmatiques du
posaconazole et adaptation éventuelle de sa posologie.
Diminution des concentrations plasmatiques et de l'efficacité du
posaconazole.
+ RIFABUTINE
Association DECONSEILLEE
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'accroissement des effets indésirables de la rifabutine
(uvéites), par augmentation de ses concentrations et de celles de
son métabolite actif.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l'efficacité des
deux anti-infectieux (induction enzymatique par la rifampicine et
diminution de l'absorption intestinale par l’azolé antifongique).
POTASSIUM
Voir aussi : hyperkaliémiants
+ ANTAGONISTES DES RÉCEPTEURS DE L'ANGIOTENSINE II
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (addition
des effets hyperkaliémiants).
+ CICLOSPORINE
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (
addition des effets hyperkaliémiants).
+ DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénal (addition
des effets hyperkaliémiants).
200
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Association DECONSEILLEE
Sauf s'il existe une hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (
addition des effets hyperkaliémiants).
+ TACROLIMUS
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (addition
des effets hyperkaliémiants).
POVIDONE IODÉE
+ ANTISEPTIQUES MERCURIELS
Association DECONSEILLEEErythèmes, phlyctènes, voire nécrose cutanéo-muqueuse
(formation d'un complexe caustique en cas d'utilisation
concomitante d'antiseptiques iodés et mercuriels). L'interaction
dépend de la stabilité de l'organo-mercuriel au niveau cutané et de
la sensibilité individuelle.
PRAVASTATINE
Voir aussi : inhibiteurs de l'HMG-CoA réductase (statines) - médicaments à l'origine d'atteintes musculaires
+ CICLOSPORINE
Précaution d'emploi
Surveillance clinique et biologique pendant l’association. Débuter le
traitement à la dose minimale de pravastatine.
Augmentation des concentrations de pravastatine, avec risque
musculaire non exclu.
+ CLARITHROMYCINE
Précaution d'emploi
Surveillance clinique et biologique pendant le traitement par
l'antibiotique.
Augmentation de la concentration plasmatique de la pravastatine
par la clarithromycine.
+ ERYTHROMYCINE
Précaution d'emploi
Surveillance clinique et biologique pendant le traitement par
l'antibiotique.
Avec l'érythromycine utilisée par voie orale : augmentation de la
concentration plasmatique de la pravastatine par l' érythromycine.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
pravastatine par augmentation de son absorption intestinale par le
ponatinib.
PRAZIQUANTEL
+ DEXAMETHASONE
Précaution d'emploi
Décaler l'administration des deux médicaments d'au moins une
semaine.
Diminution des concentrations plasmatiques du praziquantel, avec
risque d'échec du traitement, par augmentation du métabolisme
hépatique du praziquantel par la dexaméthasone.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques du
praziquantel, avec risque d'échec du traitement, par augmentation
de son métabolisme hépatique par l'inducteur.
+ RIFAMPICINE
CONTRE-INDICATIONDiminution très importante des concentrations plasmatiques du
praziquantel, avec risque d'échec du traitement, par augmentation
du métabolisme hépatique du praziquantel par la rifampicine.
PREDNISOLONE
Voir aussi : corticoïdes - corticoïdes (voie intra-articulaire) - corticoïdes métabolisés, notamment inhalés - glucocorticoïdes (sauf hydrocortisone) - hypokaliémiants -
substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ CICLOSPORINE
A prendre en compteAugmentation des effets de la prednisolone : aspect cushingoïde,
réduction de la tolérance aux glucides (diminution de la clairance
de la prednisolone).
PRÉSERVATIFS EN LATEX
+ HUILES MINÉRALES
CONTRE-INDICATION
Utiliser un lubrifiant hydrosoluble (glycérine, polyacrylamide...).
Risque de rupture du préservatif lors de l'utilisation avec des corps
gras ou des lubrifiants contenant des huiles minérales (huile de
paraffine, huile de silicone, etc...).
201
PRIMIDONE
Voir aussi : anticonvulsivants métabolisés - barbituriques - inducteurs enzymatiques - inducteurs enzymatiques puissants - médicaments sédatifs - phénobarbital (et,
par extrapolation, primidone)
+ AFATINIB
Précaution d'emploi
Surveillance clinique pendant l’association et 1 à 2 semaines après leur
arrêt.
Diminution des concentrations plasmatiques de l’afatinib par
augmentation de son métabolisme par la primidone.
PRISTINAMYCINE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la pristinamycine et après
son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ COLCHICINE
CONTRE-INDICATIONAugmentation des effets indésirables de la colchicine aux
conséquences potentiellement fatales.
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de sa posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
PROBENECIDE
+ ACIDE ACETYLSALICYLIQUE
Association DECONSEILLEEDiminution de l’effet uricosurique par compétition de l’élimination de
l’acide urique au niveau des tubules rénaux.
+ DIPROPHYLLINE
Précaution d'emploi
Réduire la posologie de diprophylline pendant le traitement par le
probénécide.
Risque de surdosage par augmentation des concentrations
plasmatiques de diprophylline (inhibition de sa sécrétion tubulaire
rénale).
+ METHOTREXATE
CONTRE-INDICATIONAugmentation de la toxicité du méthotrexate : inhibition de la
sécrétion tubulaire rénale du méthotrexate par le probénécide.
PROCARBAZINE
Voir aussi : antabuse (réaction) - cytotoxiques
+ INDUCTEURS ENZYMATIQUES PUISSANTS
A prendre en compteAugmentation des réactions d'hypersensibilité (hyperéosinophilie,
rash), par augmentation du métabolisme de la procarbazine par
l'inducteur.
PRODUITS DE CONTRASTE IODÉS
(acide amidotrizoïque, acide ioxaglique, acide ioxitalamique, iobitridol, iodixanol, iohexol, iomeprol, iopamidol, iopromide, ioversol)
+ ALDESLEUKINE
A prendre en compteMajoration du risque de réaction aux produits de contraste en cas
de traitement antérieur par interleukine 2 : éruption cutanée ou plus
rarement hypotension, oligurie voire insuffisance rénale.
+ DIURÉTIQUES
Précaution d'emploi
Réhydratation avant administration du produit iodé.
En cas de déshydratation provoquée par les diurétiques, risque
majoré d'insuffisance rénale fonctionnelle aiguë, en particulier lors
d'utilisation de doses importantes de produits de contraste iodés.
+ METFORMINE
CONTRE-INDICATION
Le traitement par la metformine doit être suspendu au moment de
l'examen radiologique pour n'être repris que 2 jours après.
Risque important d'acidose lactique par hémoconcentration de la
metformine, dans le cas d'un arrêt cardio-respiratoire induit par
l'examen radiologique, avec insuffisance rénale aiguë.
CONTRE-INDICATION
Le traitement par la metformine doit être suspendu au moment de
l'examen radiologique pour n'être repris que 2 jours après.
Risque important d'acidose lactique par hémoconcentration de la
metformine, dans le cas d'un arrêt cardio-respiratoire induit par
l'examen radiologique, avec insuffisance rénale aiguë.
CONTRE-INDICATION
Le traitement par la metformine doit être suspendu au moment de
l'examen radiologique pour n'être repris que 2 jours après.
Risque important d'acidose lactique par hémoconcentration de la
metformine, dans le cas d'un arrêt cardio-respiratoire induit par
l'examen radiologique, avec insuffisance rénale aiguë.
202
PROGESTATIFS CONTRACEPTIFS
(desogestrel, dienogest, drospirenone, etonogestrel, levonorgestrel, medroxyprogesterone, nomegestrol, norelgestromine, norethisterone, norgestimate)
+ APREPITANT
Précaution d'emploi
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique, pendant la durée de l'association et un cycle
suivant.
(Sauf stérilet), diminution des concentrations du progestatif, avec
risque de moindre efficacité contraceptive.
+ BOSENTAN
Précaution d'emploi
Utiliser une méthode contraceptive fiable, additionnelle ou alternative,
pendant la durée de l'association et un cycle suivant.
Risque de diminution de l'efficacité du contraceptif hormonal par
augmentation de son métabolisme hépatique.
+ GRISEOFULVINE
Précaution d'emploi
Utiliser une méthode contraceptive fiable, additionnelle ou alternative,
pendant la durée de l'association et un cycle suivant.
Risque de diminution de l'efficacité du contraceptif hormonal par
augmentation de son métabolisme hépatique.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEE
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique, pendant la durée de l'association et un cycle
suivant.
Diminution de l'efficacité contraceptive du contraceptif hormonal,
par augmentation de son métabolisme hépatique par l'inducteur.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Association DECONSEILLEE
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique (préservatif ou stérilet), pendant la durée de
l'association et un cycle suivant.
Risque de diminution de l'efficacité contraceptive par diminution
des concentrations en contraceptif hormonal, dûe à l'augmentation
de son métabolisme hépatique par le ritonavir.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques du contraceptif
hormonal, en raison de l'effet inducteur enzymatique du
millepertuis, avec risque de baisse d'efficacité voire d'annulation de
l'effet dont les conséquences peuvent être éventuellement graves
(survenue d'une grossesse).
+ PÉRAMPANEL
Association DECONSEILLEE
Utiliser de préférence une autre méthode contraceptive, en particulier
de type mécanique.
Pour des doses de pérampanel >= 12 mg/jour : Risque de
diminution de l’efficacité contraceptive.
+ ULIPRISTAL
Association DECONSEILLEE
- Dans l'indication contraception d'urgence:
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception additionnelle de type mécanique
pendant les 12 jours qui suivent la (dernière) prise de l’ulipristal (au cas
où il y en aurait eu plus d’une).
- Dans l’indication fibrome :
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception de type mécanique pendant les 7
premiers jours de la contraception hormonale.
Dans l'indication contraception d'urgence :
Antagonisme des effets de l’ulipristal en cas de reprise d’un
contraceptif hormonal moins de 5 jours après la prise de la
contraception d’urgence.
Dans l’indication fibrome :
Antagonisme réciproque des effets de l’ulipristal et du progestatif,
avec risque d’inefficacité.
PROGESTATIFS NON CONTRACEPTIFS, ASSOCIÉS OU NON À UN ESTROGÈNE
(chlormadinone, dydrogesterone, hydroxyprogesterone, medrogestone, medroxyprogesterone, megestrol, nomegestrol, norethisterone, progesterone, promegestone)
+ BOSENTAN
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant l’administration du bosentan et après son
arrêt.
Risque de diminution de l’efficacité du progestatif.
+ INDUCTEURS ENZYMATIQUES
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie du
traitement hormonal pendant l'administration de l'inducteur et après son
arrêt.
Diminution de l'efficacité du progestatif.
+ ULIPRISTAL
A prendre en compteDans l’indication fibrome :
Antagonisme réciproque des effets de l’ulipristal et du progestatif,
avec risque d’inefficacité.
203
PROGUANIL
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par le proguanil et après son
arrêt.
Risque d’augmentation de l’effet de l’antivitamine K et du risque
hémorragique.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par
l’antipaludique et après son arrêt.
Risque d’hypothyroïdie clinique chez les patients substitués par
hormones thyroïdiennes.
PROPAFENONE
Voir aussi : antiarythmiques
+ ABIRATERONE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
propafénone pendant le traitement par l'abiratérone.
Risque d'augmentation des effets indésirables de la propafénone,
par diminution de son métabolisme hépatique par l'abiratérone.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ BUPROPION
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
propafénone pendant le traitement par le bupropion.
Risque d'augmentation des effets indésirables de la propafénone
par diminution de son métabolisme hépatique par le bupropion.
+ CINACALCET
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par cinacalcet.
Augmentation des concentrations plasmatiques de propafénone
avec risque de surdosage, par diminution de son métabolisme
hépatique par le cinacalcet.
+ DARIFENACINE
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par darifénacine.
Augmentation des concentrations plasmatiques de propafénone,
avec risque de surdosage, par diminution de son métabolisme
hépatique par la darifénacine.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par propafénone et après son arrêt.
Risque d’augmentation de la digoxinémie, notamment chez le sujet
âgé.
+ DULOXETINE
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par la duloxétine et après son arrêt.
Augmentation des concentrations plasmatiques de propafénone
avec risque de surdosage, par diminution de son métabolisme
hépatique par la duloxétine.
+ ESMOLOL
Précaution d'emploi
Surveillance clinique et ECG.
Troubles de la contractilité, de l'automatisme et de la conduction
(suppression des mécanismes sympathiques compensateurs).
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et ECG. S'il y a lieu, adaptation de la posologie de
la propafénone pendant l'association et après l'arrêt de l'inducteur.
Diminution des concentrations plasmatiques de la propafénone par
augmentation de son métabolisme hépatique par l'inducteur.
+ MILLEPERTUIS
Précaution d'emploi
Surveillance clinique et ECG. S'il y a lieu, adaptation de la posologie de
la propafénone pendant l'association et après l'arrêt du millepertuis.
Diminution des concentrations plasmatiques de la propafénone par
augmentation de son métabolisme hépatique par le millepertuis.
+ MIRABÉGRON
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie de la
propafénone pendant l'association.
Augmentation des concentrations plasmatiques de la propafénone
par diminution de son métabolisme par le mirabégron.
204
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et ECG. S'il y a lieu, adaptation de la posologie de
la propafénone pendant l'association et après l'arrêt de la rifampicine.
Diminution des concentrations plasmatiques de la propafénone, par
augmentation de son métabolisme hépatique par la rifampicine.
+ ROLAPITANT
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par le rolapitant et après son arrêt.
Augmentation des concentrations plasmatiques de propafénone
avec risque de surdosage, par diminution de son métabolisme
hépatique par le rolapitant.
+ TERBINAFINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
propafénone pendant le traitement par la terbinafine.
Risque d'augmentation des effets indésirables de la propafénone,
par diminution de son métabolisme hépatique par la terbinafine.
+ THEOPHYLLINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Risque d’augmentation de la théophyllinémie par diminution de son
métabolisme hépatique par la propafénone.
PROPRANOLOL
Voir aussi : antihypertenseurs sauf alpha-bloquants - bradycardisants - bêta-bloquants (sauf esmolol et sotalol) (y compris collyres) - bêta-bloquants (sauf esmolol) (y
compris collyres) - bêta-bloquants non cardio-sélectifs (y compris collyres) - médicaments abaissant la pression artérielle - substances à absorption réduite par les
topiques gastro-intestinaux, antiacides et adsorbants
+ ERGOTAMINE
Précaution d'emploi
Surveillance clinique renforcée, en particulier pendant les premières
semaines de l'association.
Ergotisme : quelques cas de spasme artériel avec ischémie des
extrémités ont été observés (addition d'effets vasculaires).
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique accrue et, si besoin, adaptation de la posologie du
propranolol pendant le traitement par la fluvoxamine et après son arrêt.
Augmentation des concentrations plasmatiques de propranolol par
inhibition de son métabolisme hépatique, avec majoration de
l'activité et des effets indésirables, par exemple : bradycardie
importante.
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
A prendre en compteDiminution des concentrations plasmatiques du propranolol avec
réduction de ses effets cliniques (augmentation de son
métabolisme hépatique).
+ RIFAMPICINE
A prendre en compteDiminution des concentrations plasmatiques et de l'efficacité du
bêta-bloquant (augmentation de son métabolisme hépatique).
PYRAZINAMIDE
+ ISONIAZIDE
Précaution d'emploi
Surveillance clinique et biologique.
Addition des effets hépatotoxiques.
PYRIMETHAMINE
+ TRIMETHOPRIME
Précaution d'emploi
Contrôle régulier de l'hémogramme et association d'un traitement par
l'acide folique (injections IM régulières).
Anémie mégaloblastique, plus particulièrement à fortes doses des
deux produits (déficit en acide folique par l'association de deux 2-4
diaminopyrimidines).
QUETIAPINE
Voir aussi : médicaments abaissant le seuil épileptogène - médicaments atropiniques - médicaments sédatifs - médicaments à l'origine d'une hypotension
orthostatique - neuroleptiques - neuroleptiques antipsychotiques (sauf clozapine) - substrats à risque du CYP3A4
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
quétiapine par augmentation de son métabolisme hépatique par
l'inducteur, avec risque d’inefficacité.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation importante des concentrations de quétiapine, avec
risque de surdosage.
205
+ METHADONE
A prendre en comptePossible augmentation des concentrations de méthadone, avec
signes de surdosage.
+ MILLEPERTUIS
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
quétiapine par augmentation de son métabolisme hépatique par
l'inducteur, avec risque d’inefficacité.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la quétiapine
par diminution de son métabolisme hépatique par la bithérapie.
+ RIFAMPICINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
quétiapine par augmentation de son métabolisme hépatique par
l'inducteur, avec risque d’inefficacité.
QUINIDINE
Voir aussi : antiarythmiques - antiarythmiques classe Ia - bradycardisants - médicaments atropiniques - substances susceptibles de donner des torsades de pointes -
torsadogènes (sauf arsénieux, antiparasitaires, neuroleptiques, méthadone...)
+ ALCALINISANTS URINAIRES
Précaution d'emploi
Surveillance clinique, ECG et éventuellement contrôle de la
quinidinémie ; si besoin, adaptation de la posologie pendant le
traitement alcalinisant et après son arrêt.
Augmentation des concentrations plasmatiques de la quinidine et
risque de surdosage (diminution de l'excrétion rénale de la
quinidine par alcalinisation des urines).
+ COBICISTAT
CONTRE-INDICATION
Surveillance clinique.
Risque de majoration des effets indésirables de la quinidine par
diminution de son métabolisme par le cobicistat.
+ CODEINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ DABIGATRAN
Précaution d'emploi
Dans l'indication post-chirurgicale : surveillance clinique et adaptation
de la posologie du dabigatran à 150 mg/j en une prise.
Augmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et ECG. En cas de réponse inattendue, contrôler
la digoxinémie et adapter la posologie.
Augmentation de la digoxinémie par diminution de la clairance
rénale de la digoxine. De plus, troubles de l'automatisme
(bradycardie excessive et troubles de la conduction auriculo-
ventriculaire).
+ DRONEDARONE
Précaution d'emploi
Débuter le traitement par la quinidine aux posologies minimales
recommandées, et ajuster les doses en fonction de l’ECG.
Risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez le sujet âgé. Par ailleurs, légère augmentation des
concentrations de dronédarone par diminution de son métabolisme
par la quinidine.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ ITRACONAZOLE
Précaution d'emploi
Surveillance clinique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes, ainsi que d'acouphènes et/ou de diminution de
l'acuité auditive (cinchonisme), par diminution du métabolisme
hépatique de la quinidine.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la quinidine par
diminution de son métabolisme hépatique par la bithérapie.
+ STIRIPENTOL
Précaution d'emploi
Surveillance clinique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
206
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ TAMOXIFENE
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par la quinidine.
+ TETRABENAZINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ TRAMADOL
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ TRICLABENDAZOLE
Précaution d'emploi
Surveillance clinique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes (inhibition du métabolisme hépatique du
médicament torsadogène).
+ VERAPAMIL
Association DECONSEILLEERisque de majoration importante des effets hémodynamiques du
vérapamil, avec hypotension et bradycardie sévères.
+ VORICONAZOLE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
QUININE
Voir aussi : substrats à risque du CYP3A4
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et ECG, si besoin, avec adaptation éventuelle des
doses de digoxine.
Augmentation modérée de la digoxinémie.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la quinine
pendant le traitement par l’inducteur et après son arrêt.
Risque de perte de l’efficacité de la quinine par augmentation de
son métabolisme hépatique par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
ASDEC - PE
Association déconseillée :
- avec les inhibiteurs de protéases
Précaution d’emploi :
- avec les azolés antifongiques, certains macrolides, le tucatinib.
Surveillance clinique et ECG. Adaptation éventuelle de la posologie de
la quinine pendant le traitement par l’inhibiteur enzymatique et après
son arrêt.
Risque de majoration des effets indésirables de la quinine,
notamment troubles du rythme ventriculaire et troubles
neurosensoriels (cinchonisme).
+ MEFLOQUINE
Association DECONSEILLEE
Respecter un délai minimum de 12 heures entre la fin de
l'administration IV de quinine et le début de l'administration de
méfloquine.
Pour la quinine administrée par voie IV : risque majoré de survenue
de crises épileptiques par addition des effets proconvulsivants.
+ RIFAMPICINE
Association DECONSEILLEERisque de perte de l’efficacité de la quinine par augmentation de
son métabolisme hépatique par l’inducteur.
QUINUPRISTINE
+ DIHYDROERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
207
+ ERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l'alcaloïde de l'ergot de seigle).
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ PIMOZIDE
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
RALTÉGRAVIR
Voir aussi : inhibiteurs d'intégrase - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ RIFAMPICINE
Association DECONSEILLEE
Si l’association ne peut être évitée, un doublement de la dose de
raltégravir peut être envisagé.
Diminution des concentrations du raltégravir par la rifampicine.
RANOLAZINE
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par inhibition du métabolisme de
l'atorvastatine par la ranolazine.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique, biologique et éventuellement ECG. Adaptation de
la posologie de la digoxine, si besoin.
Augmentation de la digoxinémie.
+ IMMUNOSUPPRESSEURS
Précaution d'emploi
Surveillance clinique et biologique, et adaptation éventuelle de la
posologie de l’immunosuppresseur.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme par la
ranolazine.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEERisque de diminution importante des concentrations de ranolazine.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation des concentrations de ranolazine par diminution de
son métabolisme par l'inhibiteur.
+ RIFAMPICINE
Association DECONSEILLEEDiminution très importante des concentrations de ranolazine.
+ SIMVASTATINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par inhibition du métabolisme de la
simvastatine par la ranolazine.
RÉGORAFÉNIB
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations plasmatiques de régorafenib par
augmentation de son métabolisme par l’inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEEAugmentation des concentrations plasmatiques de régorafenib par
diminution de son métabolisme hépatique par l’inhibiteur.
208
+ MILLEPERTUIS
Association DECONSEILLEEDiminution des concentrations plasmatiques de régorafenib par
augmentation de son métabolisme par le millepertuis
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations plasmatiques de régorafenib par
diminution de son métabolisme hépatique par le pamplemousse.
REPAGLINIDE
Voir aussi : glinides
+ ANALOGUES DE LA SOMATOSTATINE
Précaution d'emploi
Renforcer l'autosurveillance glycémique et adapter si besoin la
posologie de la repaglidine pendant le traitement par l'analogue de la
somatostatine.
Risque d'hypoglycémie ou d'hyperglycémie : diminution ou
augmentation des besoins en repaglidine, par diminution ou
augmentation de la sécrétion de glucagon endogène.
+ CICLOSPORINE
Association DECONSEILLEEAugmentation de plus du double des concentrations du répaglinide
par augmentation de son absorption.
+ CLARITHROMYCINE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie de l'hypoglycémiant pendant le traitement
par la clarithromycine.
Risque d'hypoglycémie par augmentation des concentrations
plasmatiques du répaglinide.
+ CLOPIDOGREL
A prendre en compteAugmentation des concentrations du répaglinide par le clopidogrel,
avec risque de majoration des effets indésirables.
+ DEFERASIROX
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite.
Risque d’augmentation des concentrations plasmatique de
répaglinide, par inhibition de son métabolisme hépatique par le
deferasirox.
+ GEMFIBROZIL
CONTRE-INDICATIONRisque d'hypoglycémie sévère voire de coma, par augmentation
importante des concentrations plasmatiques de repaglinide par le
gemfibrozil.
+ SELPERCATINIB
Association DECONSEILLEEAugmentation importante des concentrations plasmatiques de
répaglinide, avec risque d'hypoglycémie, par diminution du
métabolisme du répaglinide par le selpercatinib.
+ TRIMETHOPRIME
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite.
Risque d’augmentation des concentrations plasmatiques de
répaglinide par inhibition de son métabolisme hépatique par le
triméthoprime.
RESERPINE
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONAgitation psychomotrice, convulsions, hypertension.
+ LEVODOPA
CONTRE-INDICATIONInhibition des effets de la lévodopa.
RÉSINES CHÉLATRICES
(colesevelam, colestyramine, polystyrène sulfonate de calcium, polystyrène sulfonate de sodium, sevelamer)
+ MÉDICAMENTS ADMINISTRÉS PAR VOIE ORALE
Précaution d'emploi
D’une façon générale, la prise de la résine doit se faire à distance de
celle des autres médicaments, en respectant un intervalle de plus de 2
heures, si possible.
La prise de résine chélatrice peut diminuer l’absorption intestinale
et, potentiellement, l’efficacité d’autres médicaments pris
simultanément.
209
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Prendre les hormones thyroïdiennes à distance de la résine (plus de 2
heures, si possible).
Diminution de l'absorption digestive des hormones thyroïdiennes.
+ ROXADUSTAT
Précaution d'emploi
Prendre le roxadustat à distance de la résine (plus de 1 heure, si
possible).
La prise de résine chélatrice peut diminuer l’absorption intestinale
et, potentiellement, l’efficacité du roxadustat pris simultanément.
RÉTINOÏDES
(acitretine, alitretinoine, isotretinoine, trétinoïne)
+ AUTRES RÉTINOÏDES
CONTRE-INDICATIONRisque de symptômes évocateurs d’une hypervitaminose A.
+ CYCLINES
CONTRE-INDICATIONRisque d'hypertension intracrânienne.
+ VITAMINE A
CONTRE-INDICATIONRisque de symptômes évocateurs d’une hypervitaminose A.
RIBAVIRINE
+ ANTIPURINES
Association DECONSEILLEERisque majoré d'effets indésirables graves, par inhibition du
métabolisme de l'immunomodulateur par la ribavirine.
+ DIDANOSINE
Association DECONSEILLEERisque de majoration de la toxicité mitochondriale de la didanosine
par augmentation de son métabolite actif.
+ STAVUDINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de diminution de l'efficacité de chaque antiviral, par
antagonisme compétitif de la réaction de phosphorylation à l'origine
des métabolites actifs.
+ ZIDOVUDINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de diminution de l'efficacité de chaque antiviral, par
antagonisme compétitif de la réaction de phosphorylation à l'origine
des métabolites actifs.
RIFABUTINE
Voir aussi : inducteurs enzymatiques
+ ATOVAQUONE
A prendre en compteDiminution modérée des concentrations plasmatiques
d'atovaquone par l'inducteur enzymatique.
+ CLARITHROMYCINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'augmentation des effets indésirables de la rifabutine
(uvéites) par augmentation de ses concentrations et de celle de
son métabolite actif par la clarithromycine. De plus, augmentation
du métabolisme de la clarithromycine par la rifabutine, avec
augmentation des concentrations de son métabolite actif.
+ COBICISTAT
Précaution d'emploi
Réduction de la dose de rifabutine (150 mg 1 jour sur deux).
Surveillance clinique et biologique régulière, notamment en début
d'association.
Augmentation très importante du métabolite de la rifabutine, avec
risque de majoration de sa toxicité (uvéites, neutropénies). Par
ailleurs, possible diminution des concentrations de cobicistat.
+ EFAVIRENZ
Précaution d'emploi
Adaptation éventuelle de la posologie de la rifabutine ou de l'éfavirenz
pendant la durée de l'association.
Diminution importante des concentrations de rifabutine, par
augmentation de son métabolisme hépatique par l’éfavirenz.
Egalement, possibilité de diminution importante des concentrations
d'éfavirenz par la rifabutine.
210
+ ELVITÉGRAVIR
A prendre en compteDiminution des concentrations minimales d’elvitégravir.
+ FLUCONAZOLE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'accroissement des effets indésirables de la rifabutine
(uvéites), par augmentation de ses concentrations et de celles de
son métabolite actif.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par la
rifabutine et après son arrêt.
Décrit pour la phénytoïne, la rifampicine, la carbamazépine. Risque
d'hypothyroïdie clinique chez les patients hypothyroïdiens, par
augmentation du métabolisme de la T3 et de la T4.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Réduction de la dose de rifabutine (150 mg 1 jour sur deux).
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de baisse de l'efficacité de l'inhibiteur de protéases (ce
d'autant que la posologie de la rifabutine est élevée) d'une part, et
risque d'augmentation des effets indésirables (uvéites) de la
rifabutine, d'autre part.
+ LÉDIPASVIR
CONTRE-INDICATIONDiminution des concentrations plasmatiques de lédipasvir par la
rifabutine, avec possible retentissement sur l’efficacité.
+ POSACONAZOLE
Association DECONSEILLEE
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque d'accroissement des effets indésirables de la rifabutine
(uvéites), par augmentation de ses concentrations et de celles de
son métabolite actif.
+ VELPATASVIR
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par la
rifabutine, avec possible retentissement sur l’efficacité.
+ VORICONAZOLE
Association DECONSEILLEE
Si l'association est jugée néccessaire, surveillance clinique et
adaptation de la posologie du voriconazole (en général doublée)
pendant le traitement par la rifabutine.
Diminution des concentrations plasmatiques du voriconazole avec
risque de perte d'efficacité, par augmentation de son métabolisme
hépatique par la rifabutine d'une part, et risque d'augmentation des
effets indésirables (uvéites) de la rifabutine d'autre part.
RIFAMPICINE
Voir aussi : inducteurs enzymatiques
+ ABIRATERONE
Association DECONSEILLEEDiminution notable des concentrations plasmatiques de
l’abiratérone, avec risque de moindre efficacité.
+ AFATINIB
Précaution d'emploi
Surveillance clinique pendant l’association et 1 à 2 semaines après leur
arrêt.
Diminution des concentrations plasmatiques de l’afatinib par
augmentation de son métabolisme par la rifampicine.
+ ALBENDAZOLE
Précaution d'emploi
Surveillance clinique de la réponse thérapeutique et adaptation
éventuelle de la posologie de l’albendazole pendant le traitement avec
l’inducteur enzymatique et après son arrêt.
Diminution importante des concentrations plasmatiques de
l’albendazole et de son métabolite actif par l’inducteur, avec risque
de baisse de son efficacité.
+ ANTAGONISTES DES CANAUX CALCIQUES
ASDEC - PE
Association déconseillée avec la nimodipine
Précaution d'emploi :
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par la rifampicine et
après son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique.
+ ANTIARYTHMIQUES CLASSE IA
Précaution d'emploi
Surveillance clinique, ECG et éventuellement de la concentration
plasmatique de l'antiarythmique. Si besoin, adaptation de la posologie
de l'antiarythmique pendant le traitement par la rifampicine et après son
arrêt (risque de surdosage en antiarythmique).
Diminution des concentrations plasmatiques et de l'efficacité de
l'antiarythmique (augmentation de son métabolisme hépatique).
211
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la rifampicine et 8 jours
après son arrêt.
Diminution de l'effet de l'antivitamine K par augmentation de son
métabolisme hépatique par la rifampicine.
+ APIXABAN
Association DECONSEILLEEDiminution des concentrations plasmatiques de l’apixaban par la
rifampicine, avec risque de diminution de l’effet thérapeutique.
+ APREPITANT
Association DECONSEILLEEDiminution très importante des concentrations d'aprépitant.
+ ATORVASTATINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques
d'atorvastatine, par augmentation de son métabolisme hépatique
par la rifampicine.
+ ATOVAQUONE
Association DECONSEILLEEDiminution des concentrations plasmatiques d'atovaquone par
l'inducteur enzymatique.
+ BICTÉGRAVIR
CONTRE-INDICATIONDiminution très importante des concentrations de bictégravir, avec
risque de perte d’efficacité.
+ BOSENTAN
Association DECONSEILLEERisque de diminution, importante pour la rifampicine, des
concentrations plasmatiques de bosentan.
+ BUSPIRONE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
buspirone pendant le traitement par rifampicine et après son arrêt.
Diminution des concentrations plasmatiques de la buspirone par
augmentation de son métabolisme hépatique par la rifampicine.
+ CANNABIDIOL
Association DECONSEILLEEDiminution des concentrations plasmatiques de cannabidiol avec
risque de perte d’efficacité.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, contrôle des concentrations plasmatiques et
adaptation de la posologie de la carbamazépine pendant le traitement
par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
carbamazépine par augmentation de son métabolisme hépatique
par la rifampicine.
+ CARVEDILOL
Précaution d'emploi
Surveillance clinique régulière et adaptation de la posologie du
carvédilol pendant le traitement par la rifampicine. A l'arrêt de la
rifampicine, risque de remontée importante des concentrations
plasmatiques de carvédilol imposant une réduction posologique et une
surveillance clinique étroite.
Diminution importante des concentrations plasmatiques du
carvédilol, par augmentation de son métabolisme hépatique par la
rifampicine.
+ CLARITHROMYCINE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Diminution des concentrations plasmatiques et risque de baisse de
l'efficacité de la clarithromycine, notamment chez le patient HIV,
par augmentation de son métabolisme hépatique par la rifampicine.
+ CLOZAPINE
Précaution d'emploi
Surveillance clinique et augmentation éventuelle de la posologie de la
clozapine durant le traitement par la rifampicine.
Risque d'inefficacité du traitement antipsychotique (diminution des
concentrations plasmatiques de clozapine par augmentation de son
métabolisme hépatique).
+ COBICISTAT
CONTRE-INDICATIONRisque de diminution de l’efficacité du cobicistat par augmentation
de son métabolisme par l’inducteur.
212
+ DABIGATRAN
Association DECONSEILLEEDiminution des concentrations plasmatiques de dabigatran, avec
risque de diminution de l'effet thérapeutique.
+ DAROLUTAMIDE
Association DECONSEILLEEDiminution des concentrations plasmatiques de dalorutamide avec
risque de perte d’efficacité.
+ DEFERASIROX
Précaution d'emploi
Surveiller la ferritinémie pendant et après le traitement par l’inducteur
enzymatique. Si besoin, adaptation de la posologie de déférasirox.
Risque de diminution des concentrations plasmatiques de
déférasirox.
+ DÉLAMANID
CONTRE-INDICATIONDiminution des concentrations plasmatiques de delamanid par
augmentation de son métabolisme hépatique par l’inducteur.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et ECG.
Diminution modeste des concentrations de digoxine.
+ DOXYCYCLINE
A prendre en compteRisque de diminution importante des concentrations de doxycycline.
+ DRONEDARONE
Association DECONSEILLEEDiminution importante des concentrations de dronédarone par
augmentation de son métabolisme, sans modification notable du
métabolite actif.
+ EFAVIRENZ
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Diminution des concentrations plasmatiques et de l'efficacité de
l'éfavirenz par augmentation de son métabolisme hépatique par la
rifampicine.
+ ESZOPICLONE
Précaution d'emploi
Surveillance clinique. Utiliser éventuellement un autre hypnotique.
Risque de diminution des concentrations plasmatiques et de
l'efficacité de l’eszopiclone par augmentation de son métabolisme
hépatique par la rifampicine.
+ EXEMESTANE
A prendre en compteRisque de diminution de l'efficacité de l'exemestane par
augmentation de son métabolisme hépatique par l'inducteur
enzymatique.
+ FENTANYL
Association DECONSEILLEE
Préférer un autre morphinique.
Diminution des concentrations plasmatiques de fentanyl par
augmentation de son métabolisme hépatique par la rifampicine.
+ FLUCONAZOLE
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l'efficacité du
fluconazole par augmentation de son métabolisme par la
rifampicine.
+ HALOPERIDOL
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique pendant le
traitement par la rifampicine et après son arrêt.
Risque de diminution des concentrations plasmatiques de
l'halopéridol et de son efficacité thérapeutique, par augmentation
de son métabolisme hépatique par la rifampicine.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique. Adaptation, si besoin, de la
posologie des hormones thyroïdiennes pendant le traitement par la
rifampicine et après son arrêt.
Risque d'hypothyroïdie clinique chez les patients hypothyroïdiens,
par augmentation du métabolisme de la T3 et de la T4.
+ IDÉLALISIB
Association DECONSEILLEEDiminution des concentrations plasmatiques d’idélalisib par
augmentation de son métabolisme hépatique par l’inducteur.
213
+ INHIBITEURS DE LA 5-ALPHA REDUCTASE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Diminution des concentrations plasmatiques de l’inhibiteur de la 5-
alpha réductase par l’inducteur enzymatique.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
CONTRE-INDICATION
Dans l'attente de données complémentaires avec les inhibiteurs de
protéases "boostés".
Diminution très importante des concentrations plasmatiques de
l'inhibiteur de protéases, par augmentation de son métabolisme
hépatique par la rifampicine.
Pour l'association (saquinavir + ritonavir) :
risque de toxicité hépatocellulaire sévère.
+ INHIBITEURS DE TYROSINE KINASES MÉTABOLISÉS
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l’efficacité de
l’inhibiteur de tyrosine kinase, par augmentation de son
métabolisme par l’inducteur.
+ ISONIAZIDE
Précaution d'emploi
Surveillance clinique et biologique de cette association classique. En
cas d'hépatite, arrêter l'isoniazide.
Augmentation de l'hépatotoxicité de l'isoniazide (augmentation de
la formation de métabolites toxiques de l'isoniazide).
+ IVABRADINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’ivabradine
pendant l’association et après l’arrêt de la rifampicine.
Risque de diminution de l'efficacité de l’ivabradine, par
augmentation de son métabolisme par la rifampicine.
+ KETOCONAZOLE
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l'efficacité des
deux anti-infectieux (induction enzymatique par la rifampicine et
diminution de l'absorption intestinale par l’azolé antifongique).
+ LÉDIPASVIR
CONTRE-INDICATIONDiminution importante des concentrations plasmatiques du
lédipasvir par augmentation de son métabolisme hépatique par la
rifampicine.
+ LÉNACAPAVIR
CONTRE-INDICATIONDiminution, éventuellement considérable, des concentrations de
lénacapavir, avec risque de réduction de la réponse virologique.
+ LINEZOLIDE
Précaution d'emploi
Surveillance clinique et augmentation éventuelle de la posologie du
linézolide pendant le traitement par la rifampicine.
Risque de diminution de l'efficacité du linézolide par augmentation
de son métabolisme hépatique par la rifampicine.
+ METOPROLOL
A prendre en compteDiminution des concentrations plasmatiques et de l'efficacité du
bêta-bloquant (augmentation de son métabolisme hépatique).
+ METRONIDAZOLE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
métronidazole pendant le traitement par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques du métronidazole par
augmentation de son métabolisme hépatique par la rifampicine.
+ MIDAZOLAM
Association DECONSEILLEERisque d'absence d'effet du midazolam, avec diminution très
importante de ses concentrations plasmatiques, par augmentation
de son métabolisme hépatique.
+ MINÉRALOCORTICOÏDES
Précaution d'emploi
Surveillance clinique et biologique ; adaptation de la posologie des
corticoïdes pendant le traitement par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité des
corticoïdes par augmentation de leur métabolisme hépatique par la
rifampicine ; les conséquences sont particulièrement importantes
chez les addisoniens traités par l'hydrocortisone et en cas de
transplantation.
+ MONTELUKAST
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de
l'antiasthmatique pendant le traitement par la rifampicine et après son
arrêt.
Risque de baisse de l'efficacité du montélukast par augmentation
de son métabolisme hépatique par la rifampicine.
214
+ MORPHINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
morphine pendant le traitement par la rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
morphine et de son métabolite actif.
+ NEVIRAPINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de la névirapine par
augmentation de son métabolisme hépatique par la rifampicine.
+ NIMODIPINE
Association DECONSEILLEE
Surveillance clinique et adaptation éventuelle de la posologie de
l'antagoniste du calcium pendant le traitement par la rifampicine et
après son arrêt.
Diminution des concentrations plasmatiques de l'antagoniste du
calcium par augmentation de son métabolisme hépatique.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Diminution des concentrations plasmatiques du nintédanib par
diminution de son absorption par la rifampicine.
+ OZANIMOD
Association DECONSEILLEEDiminution des concentrations des métabolites actifs de l’ozanimod
d’environ 60%.
+ PÉRAMPANEL
A prendre en compteDiminution importante (jusqu’aux deux-tiers) des concentrations de
pérampanel.
+ POSACONAZOLE
Association DECONSEILLEEDiminution des concentrations plasmatiques et de l'efficacité des
deux anti-infectieux (induction enzymatique par la rifampicine et
diminution de l'absorption intestinale par l’azolé antifongique).
+ PRAZIQUANTEL
CONTRE-INDICATIONDiminution très importante des concentrations plasmatiques du
praziquantel, avec risque d'échec du traitement, par augmentation
du métabolisme hépatique du praziquantel par la rifampicine.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et ECG. S'il y a lieu, adaptation de la posologie de
la propafénone pendant l'association et après l'arrêt de la rifampicine.
Diminution des concentrations plasmatiques de la propafénone, par
augmentation de son métabolisme hépatique par la rifampicine.
+ PROPRANOLOL
A prendre en compteDiminution des concentrations plasmatiques et de l'efficacité du
bêta-bloquant (augmentation de son métabolisme hépatique).
+ QUETIAPINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
quétiapine par augmentation de son métabolisme hépatique par
l'inducteur, avec risque d’inefficacité.
+ QUININE
Association DECONSEILLEERisque de perte de l’efficacité de la quinine par augmentation de
son métabolisme hépatique par l’inducteur.
+ RALTÉGRAVIR
Association DECONSEILLEE
Si l’association ne peut être évitée, un doublement de la dose de
raltégravir peut être envisagé.
Diminution des concentrations du raltégravir par la rifampicine.
+ RANOLAZINE
Association DECONSEILLEEDiminution très importante des concentrations de ranolazine.
+ RIVAROXABAN
Association DECONSEILLEEDiminution des concentrations plasmatiques de rivaroxaban, avec
risque de diminution de l'effet thérapeutique.
215
+ SACITUZUMAB
A prendre en comptePour le SN38 lié au sacizutumab (govitécan) : risque de diminution
de son exposition, par augmentation de son métabolisme.
+ SIMVASTATINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
simvastatine, par augmentation de son métabolisme hépatique par
la rifampicine.
+ SOTORASIB
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du sotorasib,
avec risque de moindre efficacité.
+ TELITHROMYCINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de la
télithromycine, avec risque d'échec du traitement anti-infectieux,
par augmentation du métabolisme hépatique de la télithromycine
par la rifampicine.
+ TÉNOFOVIR ALAFÉNAMIDE
Association DECONSEILLEE
Surveillance clinique pendant l’association et 1 à 2 semaines après
l’arrêt de la rifampicine.
Diminution des concentrations plasmatiques du ténofovir
alafénamide par diminution de son absorption par la rifampicine.
+ TERBINAFINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
terbinafine pendant le traitement par la rifampicine.
Diminution des concentrations plasmatiques et de l'efficacité de la
terbinafine, par augmentation de son métabolisme hépatique par la
rifampicine.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et, si besoin, de la théophyllinémie. Adapter, s'il y
a lieu, la posologie de la théophylline pendant le traitement par la
rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
théophylline (augmentation de son métabolisme par induction
enzymatique).
+ TIAGABINE
Précaution d'emploi
Une augmentation de la posologie de la tiagabine peut s’avérer
nécessaire en cas d’association à la rifampicine.
Diminution des concentrations plasmatiques de la tiagabine par
augmentation de son métabolisme hépatique.
+ TICAGRELOR
Association DECONSEILLEEDiminution importante des concentrations plasmatiques de
ticagrelor par augmentation de son métabolisme hépatique par la
rifampicine, avec risque de diminution de l’effet thérapeutique.
+ ULIPRISTAL
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par l’inducteur.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique et biologique, et adaptation éventuelle de la
posologie de l'anticonvulsivant pendant le traitement par la rifampicine
et après son arrêt.
Risque de survenue de crises convulsives, par augmentation du
métabolisme hépatique du valproate par la rifampicine.
+ VELPATASVIR
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par la
rifampicine, avec possible retentissement sur l’efficacité.
+ VITAMINE D
Précaution d'emploi
Dosage des concentrations de vitamine D et supplémentation si
nécessaire.
Diminution des concentrations de vitamine D plus marquée qu’en
l’absence de traitement par la rifampicine
+ VORICONAZOLE
CONTRE-INDICATIONDiminution importante des concentrations plasmatiques du
voriconazole avec risque de perte d'efficacité, par augmentation de
son métabolisme hépatique par la rifampicine.
+ VOXELOTOR
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du voxelotor,
avec risque de moindre efficacité.
216
+ ZIDOVUDINE
Association DECONSEILLEE
Si l'association s'avère nécessaire, surveillance clinique et biologique
renforcée.
Diminution de moitié des concentrations de la zidovudine par
augmentation de son métabolisme par la rifampicine.
+ ZOLPIDEM
Précaution d'emploi
Surveillance clinique. Utiliser éventuellement un autre hypnotique.
Diminution des concentrations plasmatiques et de l'efficacité du
zolpidem par augmentation de son métabolisme hépatique par la
rifampicine.
+ ZOPICLONE
Précaution d'emploi
Surveillance clinique. Utiliser éventuellement un autre hypnotique.
Diminution des concentrations plasmatiques et de l'efficacité de la
zopiclone par augmentation de son métabolisme hépatique par la
rifampicine.
RILPIVIRINE
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compte
Si nécessaire, utiliser un antihistaminique H2 actif en une prise par jour,
à prendre au moins 12 heures avant, ou au moins 4 heures après.
Risque de diminution des concentrations plasmatiques de la
rilpivirine.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de rilpivirine par
l’inhibiteur de la pompe à protons (absorption diminuée en raison
de l’augmentation du pH gastrique).
+ DEXAMETHASONE
CONTRE-INDICATIONAvec la dexaméthasone par voie systémique (sauf en cas de prise
unique), risque de diminution des concentrations plasmatiques de
rilpivirine par augmentation de son métabolisme hépatique par la
dexamethasone.
+ INDUCTEURS ENZYMATIQUES
CONTRE-INDICATIONDiminution significative des concentrations plasmatiques de
rilpivirine par augmentation de son métabolisme hépatique par
l’inducteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
rilpivirine par augmentation de son métabolisme hépatique par le
millepertuis.
RIOCIGUAT
Voir aussi : médicaments à l'origine d'une hypotension orthostatique
+ DÉRIVÉS NITRÉS ET APPARENTÉS
CONTRE-INDICATIONRisque d'hypotension importante (effet synergique).
+ INHIBITEURS DE LA PHOSPHODIESTERASE DE TYPE 5
CONTRE-INDICATIONRisque d'hypotension importante (effet synergique).
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEEAugmentation des concentrations plasmatiques de riociguat par
diminution de son métabolisme hépatique par l’inhibiteur.
RISPERIDONE
Voir aussi : médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - neuroleptiques - neuroleptiques antipsychotiques (sauf clozapine)
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique de la
rispéridone.
Risque de diminution de la fraction active de la rispéridone et de
son efficacité thérapeutique par augmentation de son métabolisme
hépatique par la carbamazépine.
+ FLUOXETINE
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique de la
rispéridone.
Augmentation de la fraction active de la rispéridone par diminution
de son métabolisme hépatique par la fluoxétine, avec risque de
majoration des effets indésirables.
217
+ PAROXETINE
Précaution d'emploi
Surveillance clinique et, si besoin, adaptation posologique de la
rispéridone.
Augmentation de la fraction active de la rispéridone par diminution
de son métabolisme hépatique par la paroxétine, avec risque de
majoration des effets indésirables.
RITONAVIR
Voir aussi : inhibiteurs de protéases boostés par ritonavir - inhibiteurs puissants du CYP3A4
+ CORTICOÏDES (VOIE INTRA-ARTICULAIRE)
A prendre en compte
Préférer un corticoïde non CYP3A4-dépendant (hydrocortisone)
Décrit chez des patients HIV.
Risque d’insuffisance surrénale aiguë, même en cas d’injection
unique.
L’articulation peut constituer un réservoir relarguant de façon
continue le corticoïde CYP3A4-dépendant dans la circulation
générale, avec augmentation possiblement très importante des
concentrations du corticoïde à l’origine d’une freination de la
réponse hypothalamo-hypophysaire.
+ GLUCOCORTICOÏDES PAR VOIE INTRA-ARTICULAIRE ET MÉTABOLISÉS
Précaution d'emploi
Préférer un corticoïde non CYP3A4-dépendant (hydrocortisone).
Décrit chez des patients HIV.
Risque d’insuffisance surrénale aiguë, même en cas d’injection
unique. L’articulation peut constituer un réservoir relarguant de
façon continue le corticoïde CYP3A4-dépendant dans la circulation
générale, avec augmentation possiblement très importante des
concentrations du corticoïde, à l’origine d’une freination de la
réponse hypothalamo-hypophysaire.
RIVAROXABAN
Voir aussi : anticoagulants oraux - substrats à risque du CYP3A4
+ FLUCONAZOLE
Association DECONSEILLEEAugmentation des concentrations plasmatiques du rivaroxaban par
le fluconazole, avec majoration du risque de saignement.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques de rivaroxaban, avec
risque de diminution de l'effet thérapeutique.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEEAugmentation des concentrations plasmatiques de rivaroxaban,
avec majoration du risque de saignement.
+ RIFAMPICINE
Association DECONSEILLEEDiminution des concentrations plasmatiques de rivaroxaban, avec
risque de diminution de l'effet thérapeutique.
ROLAPITANT
+ COLCHICINE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des effets indésirables de la colchicine, aux
conséquences potentiellement fatales.
+ DABIGATRAN
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
dabigatran par augmentation de son absorption intestinale par le
rolapitant.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et ECG pendant le traitement par le rolapitant et
après son arrêt.
Augmentation de la digoxinémie par majoration de son absorption.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution très importante des concentrations de rolapitant avec
risque de perte d’efficacité.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par le rolapitant.
Chez l'insuffisant cardiaque, risque d'augmentation des effets
indésirables du métoprolol, par diminution de son métabolisme
hépatique par le rolapitant.
218
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution très importante des concentrations de rolapitant avec
risque de perte d’efficacité.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et réduction de la posologie de la propafénone
pendant le traitement par le rolapitant et après son arrêt.
Augmentation des concentrations plasmatiques de propafénone
avec risque de surdosage, par diminution de son métabolisme
hépatique par le rolapitant.
+ ROSUVASTATINE
Précaution d'emploi
Utiliser la rosuvastatine à dose minimale.
Risque d’augmentation des concentrations de rosuvastatine.
+ TAMOXIFENE
Association DECONSEILLEERisque de baisse de l’efficacité du tamoxifène par inhibition de la
formation de son métabollite actif par le rolapitant.
ROPINIROLE
Voir aussi : antiparkinsoniens dopaminergiques - dopaminergiques - médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - médicaments à
risque lors du sevrage tabagique
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l’INR. Adaptation éventuelle de la posologie
de l’antivitamine K pendant le traitement par ropinirole et après son
arrêt.
Augmentation du risque hémorragique.
+ CIPROFLOXACINE
Précaution d'emploi
Surveillance clinique et réduction éventuelle de la posologie du
ropinirole pendant le traitement par la ciprofloxacine et après son arrêt.
Augmentation des concentrations de ropinirole avec risque de
surdosage, par diminution de son métabolisme hépatique par la
ciprofloxacine.
+ ENOXACINE
Précaution d'emploi
Surveillance clinique et réduction de la posologie du ropinirole pendant
le traitement par l'énoxacine et après son arrêt.
Augmentation des concentrations plasmatiques de ropinirole avec
signes de surdosage par diminution de son métabolisme hépatique.
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique et réduction de la posologie du ropinirole pendant
le traitement par fluvoxamine et après son arrêt.
Augmentation des concentrations de ropinirole, avec risque de
surdosage, par diminution de son métabolisme hépatique par la
fluvoxamine.
ROSUVASTATINE
Voir aussi : inhibiteurs de l'HMG-CoA réductase (statines) - médicaments à l'origine d'atteintes musculaires - substances à absorption réduite par les topiques gastro-
intestinaux, antiacides et adsorbants
+ CICLOSPORINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, ou de néphrotoxicité, par diminution du
métabolisme de la rosuvastatine.
+ DAROLUTAMIDE
Association DECONSEILLEEAugmentation considérable (d’un facteur 5) des concentrations de
rosuvastatine avec risque de rhabdomyolyse et/ou de
néphrotoxicité, par augmentation de sa biodisponibilité.
+ FOSTAMATINIB
Précaution d'emploi
Surveillance clinique et biologique, avec adaptation de la posologie de
rosuvastatine si nécessaire.
Doublement moyen des concentrations plasmatiques de la
rosuvastatine.
+ FOSTEMSAVIR
Précaution d'emploi
Débuter par la dose minimale de rosuvastatine. Surveillance clinique
régulière.
Augmentation modérée des concentrations de rosuvastatine.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique et biologique.
Augmentation des concentrations plasmatiques de la rosuvastatine
par augmentation de son absorption.
219
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
rosuvastatine par augmentation de son absorption intestinale par le
ponatinib.
+ ROLAPITANT
Précaution d'emploi
Utiliser la rosuvastatine à dose minimale.
Risque d’augmentation des concentrations de rosuvastatine.
+ TÉDIZOLIDE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de la
rosuvastatine, par augmentation de son absorption avec le
tédizolide administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
+ VELPATASVIR
Précaution d'emploi
En cas d’association, ne pas dépasser 10 mg par jour de rosuvastatine.
Augmentation des concentrations plasmatiques de rosuvastatine
par augmentation de son absorption intestinale par le velpatasvir.
ROXADUSTAT
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ CALCIUM
Précaution d'emploi
Prendre le roxadustat à distance des sels de calcium (plus de 1 heure,
si possible).
La prise de cation divalent peut diminuer l’absorption intestinale et,
potentiellement, l’efficacité du roxadustat pris simultanément.
+ FER
Précaution d'emploi
Prendre le roxadustat à distance des sels de fer (plus de 1 heure, si
possible).
La prise de cation divalent peut diminuer l’absorption intestinale et,
potentiellement, l’efficacité du roxadustat pris simultanément.
+ GEMFIBROZIL
Précaution d'emploi
Surveillance clinique et biologique (hémoglobine).
Augmentation de l’exposition du roxadustat, par diminution de son
métabolisme par le gemfibrozil.
+ INHIBITEURS DE L'HMG-COA RÉDUCTASE (STATINES)
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la statine pendant
le traitement par roxadustat.
Augmentation d’un facteur 2 à 3 de l’exposition de la statine, par
diminution de son métabolisme par le roxadustat.
+ MAGNÉSIUM
Précaution d'emploi
Prendre le roxadustat à distance des sels de magnésium (plus de 1
heure, si possible).
La prise de cation divalent peut diminuer l’absorption intestinale et,
potentiellement, l’efficacité du roxadustat pris simultanément.
+ RÉSINES CHÉLATRICES
Précaution d'emploi
Prendre le roxadustat à distance de la résine (plus de 1 heure, si
possible).
La prise de résine chélatrice peut diminuer l’absorption intestinale
et, potentiellement, l’efficacité du roxadustat pris simultanément.
ROXITHROMYCINE
Voir aussi : macrolides (sauf spiramycine)
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse.
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après l'arrêt du macrolide.
Risque d'augmentation des concentrations sanguines de
ciclosporine et de la créatininémie.
+ MIDAZOLAM
A prendre en compteMajoration légère de la sédation.
220
+ SIMVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse.
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
A prendre en compteRisque d'augmentation de la théophyllinémie, particulièrement chez
l'enfant.
RUFINAMIDE
+ ESTROPROGESTATIFS CONTRACEPTIFS
Précaution d'emploi
Utiliser une méthode additionnelle de type mécanique (préservatif)
pendant la durée de l’association, et un cycle suivant l’arrêt du
rufinamide.
Diminution de l’efficacité contraceptive par augmentation du
métabolisme hépatique du contraceptif hormonal par le rufinamide.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Chez l’enfant de moins de 30 kg :
ne pas dépasser la dose totale de 600 mg/j après la période de titration.
Possible augmentation des concentrations de rufinamide,
notamment chez l’enfant de moins de 30 kg.
SACITUZUMAB
+ INDUCTEURS ENZYMATIQUES PUISSANTS
A prendre en comptePour le SN38 lié au sacizutumab (govitécan) : risque de diminution
de son exposition, par augmentation de son métabolisme.
+ RIFAMPICINE
A prendre en comptePour le SN38 lié au sacizutumab (govitécan) : risque de diminution
de son exposition, par augmentation de son métabolisme.
SACUBITRIL
Voir aussi : médicaments, bradykinine et angio-œdème
+ INHIBITEURS DE L'ENZYME DE CONVERSION
CONTRE-INDICATIONAugmentation du risque d'angioedème.
SALMETEROL
+ ITRACONAZOLE
A prendre en compteAugmentation importante des concentrations de salmétérol par
diminution de son métabolisme hépatique par l'itraconazole.
+ KETOCONAZOLE
A prendre en compteAugmentation importante des concentrations de salmétérol par
diminution de son métabolisme hépatique par le kétoconazole.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONRisque d’augmentation des concentrations de salmétérol.
SELEXIPAG
+ CLOPIDOGREL
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
+ DEFERASIROX
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
221
+ GEMFIBROZIL
CONTRE-INDICATIONRisque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
+ TÉRIFLUNOMIDE
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
+ TRIMETHOPRIME
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
SELPERCATINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Surveillance clinique et biologique, et adjonction éventuelle de
liothyronine au traitement par la lévothyroxine.
Risque de moindre efficacité de la supplémentation en
lévothyroxine par baisse de la conversion de T4 en T3 en cas de
traitement par selpercatinib.
+ REPAGLINIDE
Association DECONSEILLEEAugmentation importante des concentrations plasmatiques de
répaglinide, avec risque d'hypoglycémie, par diminution du
métabolisme du répaglinide par le selpercatinib.
SERTRALINE
Voir aussi : hyponatrémiants - inhibiteurs sélectifs de la recapture de la sérotonine - médicaments abaissant le seuil épileptogène - médicaments à l'origine d'un
syndrome sérotoninergique
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEERisque d’inefficacité du traitement antidépresseur.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation parfois importante des concentrations de
l’antidépresseur chez certains patients par diminution de son
métabolisme intestinal.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
SÉTRONS
(granisetron, ondansetron, palonosetron)
+ APOMORPHINE
CONTRE-INDICATIONDes hypotensions sévères et des pertes de connaissance ont été
rapportées lors de l’association d’un sétron avec l’apomorphine.
SILDENAFIL
Voir aussi : inhibiteurs de la phosphodiesterase de type 5 - médicaments à l'origine d'une hypotension orthostatique
+ JOSAMYCINE
Précaution d'emploi
Débuter le traitement par sildénafil à la dose minimale en cas
d'association avec la josamycine.
Augmentation des concentrations plasmatiques de sildénafil, avec
risque d'hypotension.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du sildénafil par
diminution de son métabolisme hépatique par la bithérapie.
SILODOSINE
Voir aussi : alphabloquants à visée urologique - médicaments à l'origine d'une hypotension orthostatique
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEERisque d’augmentation des effets indésirables de la silodosine par
l’inhibiteur, notamment à type d’hypotension orthostatique.
222
SIMVASTATINE
Voir aussi : inhibiteurs de l'HMG-CoA réductase (statines) - médicaments à l'origine d'atteintes musculaires - substrats à risque du CYP3A4
+ AMIODARONE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
simvastatine).
+ AMLODIPINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
+ APALUTAMIDE
Association DECONSEILLEERisque de diminution très importante des concentrations de la
simvastatine, et perte d‘efficacité, par augmentation de son
métabolisme hépatique par l’apalutamide.
+ AZITHROMYCINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant ou une autre
statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ CARBAMAZEPINE
Association DECONSEILLEEDiminution importante des concentrations plasmatiques de
simvastatine, par augmentation de son métabolisme hépatique.
+ CICLOSPORINE
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par diminution du métabolisme de la
simvastatine.
+ DANAZOL
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par diminution du métabolisme de la
simvastatine.
+ DILTIAZEM
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/jour de simvastatine. Si
l'objectif thérapeutique n'est pas atteint à cette posologie, utiliser une
autre statine non concernée par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ DRONEDARONE
Association DECONSEILLEERisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
simvastatine).
+ FLUCONAZOLE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d’interaction.
Risque majoré d'effets indésirables concentration-dépendants à
type de rhabdomyolyse (diminution du métabolisme hépatique de la
simvastatine).
+ GLÉCAPRÉVIR + PIBRENTASVIR
CONTRE-INDICATIONAugmentation importante des concentrations plasmatiques de
simvastatine par la bithérapie, avec risque majoré d’effets
indésirables (concentration-dépendants) à type de rhabdomyolyses .
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONRisque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par diminution du métabolisme de la
simvastatine.
+ MILLEPERTUIS
Association DECONSEILLEEDiminution de l’efficacité de l’hypocholestérolémiant par
augmentation de son métabolisme hépatique par le millepertuis.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de la simvastatine
par diminution de son métabolisme hépatique par la bithérapie.
223
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation considérable des concentrations plasmatiques de
l'hypolipémiant, avec risque de survenue d'effets indésirables,
notamment musculaires.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
simvastatine par augmentation de son absorption intestinale par le
ponatinib.
+ RANOLAZINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse par inhibition du métabolisme de la
simvastatine par la ranolazine.
+ RIFAMPICINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de
simvastatine, par augmentation de son métabolisme hépatique par
la rifampicine.
+ ROXITHROMYCINE
Précaution d'emploi
Utiliser des doses plus faibles d’hypocholestérolémiant.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse.
+ STIRIPENTOL
CONTRE-INDICATIONRisque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
+ VERAPAMIL
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
SIROLIMUS
Voir aussi : immunosuppresseurs - médicaments, bradykinine et angio-œdème - substrats à risque du CYP3A4
+ CICLOSPORINE
Précaution d'emploi
Il est recommandé d’administrer le sirolimus 4 heures après la
ciclosporine. Contrôle de la fonction rénale, pendant l’association et
après son arrêt.
Augmentation des concentrations sanguines de sirolimus par la
ciclosporine. La néphrotoxicité de la ciclosporine est également
augmentée lors de l’association.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
A prendre en compteMajoration du risque d’angio-oedème.
+ OMBITASVIR + PARITAPRÉVIR
Association DECONSEILLEE
Si l’association s’avère nécessaire, contrôle strict de la fonction rénale,
dosage des concentrations sanguines de l'immunosuppresseur et
adaptation éventuelle de la posologie.
En association avec le ritonavir : augmentation significative des
concentrations de l’immunosuppresseur avec risque de majoration
de sa toxicité par la bithérapie.
+ VERAPAMIL
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines du sirolimus
(diminution de son métabolisme hépatique par le vérapamil).
SODIUM (BICARBONATE DE)
Voir aussi : alcalinisants urinaires
+ LITHIUM
Précaution d'emploi
Eviter les surcharges sodées et tenir compte de la présence de sodium
dans certains médicaments comme les antiacides.
Risque de baisse de l’efficacité du lithium par augmentation de son
élimination rénale par les sels de sodium.
SODIUM (CHLORURE DE)
+ LITHIUM
Précaution d'emploi
Eviter les surcharges sodées et tenir compte de la présence de sodium
dans certains médicaments comme les antiacides.
Risque de baisse de l’efficacité du lithium par augmentation de son
élimination rénale par les sels de sodium.
224
SOFOSBUVIR
+ AMIODARONE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique et ECG étroite,
en particulier pendant les premières semaines de traitement. Une
surveillance continue en milieu hospitalier est requise pendant les 48
heures qui suivent la co-adminsitration.
Prendre en compte la longue demi-vie de l'amiodarone chez les
patients l'ayant arrêtée au cours des derniers mois et qui doivent
débuter un traitement contenant du sofosbuvir.
Survenue de bradycardie éventuellement brutale, pouvant avoir des
conséquences fatales.
+ INDUCTEURS ENZYMATIQUES
CI - ASDEC
Contre-indication :
- avec la rifampicine
- avec les anticonvulsivants inducteurs enzymatiques
Association déconseillée:
- avec les autres inducteurs.
Risque de diminution des concentrations plasmatiques de
sofosbuvir par diminution de son absorption intestinale par
l’inducteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
sofosbuvir par diminution de son absorption intestinale par
le millepertuis.
SORBITOL
+ LAMIVUDINE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance plus fréquente de la
charge virale.
Diminution des concentrations plasmatiques de lamivudine par le
sorbitol.
+ POLYSTYRÈNE SULFONATE DE CALCIUM
CONTRE-INDICATIONPar voie orale ou rectale du sorbitol ou de la résine, et pour une
dose de sorbitol par prise >= 2,5 g chez l'enfant et 5 g chez l'adulte :
Risque de nécrose colique, éventuellement fatale.
+ POLYSTYRÈNE SULFONATE DE SODIUM
CONTRE-INDICATIONPar voie orale ou rectale du sorbitol ou de la résine, et pour une
dose de sorbitol par prise >= 2,5 g chez l'enfant et 5 g chez l'adulte :
Risque de nécrose colique, éventuellement fatale.
SOTORASIB
Voir aussi : inducteurs enzymatiques
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compteRisque de diminution de l’effet du sotorasib, par diminution de son
absorption.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compteRisque de diminution de l’effet du sotorasib, par diminution de son
absorption.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du sotorasib,
avec risque de moindre efficacité.
+ RIFAMPICINE
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du sotorasib,
avec risque de moindre efficacité.
SPERMICIDES
(benzalkonium, cetalkonium, nonoxynol 9)
+ MÉDICAMENTS UTILISÉS PAR VOIE VAGINALE
Association DECONSEILLEETout traitement local vaginal est susceptible d'inactiver une
contraception locale spermicide.
225
SPIRAMYCINE
Voir aussi : substances susceptibles de donner des torsades de pointes - torsadogènes (sauf arsénieux, antiparasitaires, neuroleptiques, méthadone...)
+ LEVODOPA
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de la
lévodopa.
En cas d'association avec la carbidopa : inhibition de l'absorption
de la carbidopa avec diminution des concentrations plasmatiques
de la lévodopa.
SPIRONOLACTONE
Voir aussi : antihypertenseurs sauf alpha-bloquants - diurétiques - diurétiques épargneurs de potassium (seuls ou associés) - hyperkaliémiants - hyponatrémiants -
médicaments abaissant la pression artérielle
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Précaution d'emploi
Vérifier au préalable l’absence d’hyperkaliémie et d’insuffisance rénale.
Surveillance biologique étroite de la kaliémie et de la créatininémie (1
fois par semaine pendant le premier mois, puis une fois par mois
ensuite).
Avec la spironolactone à la posologie de 12,5 à 50 mg par jour, et
avec des doses faibles d’IEC.
Dans le traitement de l’insuffisance cardiaque de classe III ou IV
(NYHA) avec fraction d’éjection <35 % et préalablement traitée par
l’association inhibiteur de conversion + diurétique de l’anse : risque
d’hyperkaliémie, potentiellement létale, en cas de non-respect des
conditions de prescription de cette association.
+ MITOTANE
CONTRE-INDICATIONPossible réduction voire abolition de l'effet pharmacodynamique du
mitotane par la spironolactone, associé à une baisse des
concentrations du mitotane.
STAVUDINE
+ ISONIAZIDE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
+ PENTAMIDINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
+ RIBAVIRINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de diminution de l'efficacité de chaque antiviral, par
antagonisme compétitif de la réaction de phosphorylation à l'origine
des métabolites actifs.
+ THALIDOMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
+ ZIDOVUDINE
Association DECONSEILLEERisque de diminution de l'efficacité de chaque antiviral par
antagoniste compétitif de la réaction de phosphorylation à l'origine
des métabolites actifs.
STIRIPENTOL
+ ATORVASTATINE
CONTRE-INDICATIONRisque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
+ CAFEINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle de la posologie de caféine.
Augmentation possible des concentrations plasmatiques de la
caféine, avec risque de surdosage, par inhibition de son
métabolisme hépatique.
+ CLOBAZAM
Précaution d'emploi
Surveillance clinique, dosage plasmatique, lorsque cela est possible, de
l'anticonvulsivant associé au stiripentol et éventuelle adaptation
posologique de l'anticonvulsivant associé.
Augmentation des concentrations plasmatiques de ces
anticonvulsivants, avec risque de surdosage, par inhibition de leur
métabolisme hépatique.
+ DIAZEPAM
Précaution d'emploi
Surveillance clinique et dosage plasmatique, lorsque cela est possible,
de l'anticonvulsivant associé au stiripentol et éventuelle adaptation
posologique de l'anticonvulsivant associé.
Augmentation des concentrations plasmatiques du diazépam, avec
risque de surdosage, par inhibition de son métabolisme hépatique.
226
+ DIHYDROERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition de
l’élimination hépatique de l'alcaloïde de l’ergot de seigle).
+ ERGOTAMINE
CONTRE-INDICATIONErgotisme avec possibilité de nécrose des extrémités (inhibition de
l’élimination hépatique de l'alcaloïde de l’ergot de seigle).
+ HALOFANTRINE
Association DECONSEILLEERisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ IMMUNOSUPPRESSEURS
CONTRE-INDICATIONAugmentation des concentrations sanguines de
l’immunosuppresseur (diminution de son métabolisme hépatique).
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et dosage plasmatique, lorsque cela est possible,
de l'inducteur associé au stiripentol et adaptation éventuelle de sa
posologie.
Augmentation des concentrations plasmatiques de l'inducteur, avec
risque de surdosage, par inhibition de son métabolisme hépatique
par le stiripentol.
+ MIDAZOLAM
Précaution d'emploi
Surveillance clinique et réduction de la posologie pendant le traitement
par le stiripentol.
Augmentation des concentrations plasmatiques du midazolam par
diminution de son métabolisme hépatique avec majoration de la
sédation.
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ QUINIDINE
Précaution d'emploi
Surveillance clinique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SIMVASTATINE
CONTRE-INDICATIONRisque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique, dosage plasmatique et adaptation éventuelle de la
posologie de théophylline.
Augmentation possible de la théophyllinémie, avec risque de
surdosage, par inhibition de son métabolisme hépatique.
STRONTIUM
+ CALCIUM
Précaution d'emploi
Prendre le strontium à distance des sels de calcium (plus de deux
heures, si possible).
Avec les sels de calcium administrés par voie orale : diminution de
l'absorption digestive du strontium.
+ CYCLINES
Précaution d'emploi
Prendre le strontium à distance des cyclines (plus de deux heures, si
possible).
Diminution de l'absorption digestive du strontium.
+ FER
Précaution d'emploi
Prendre le strontium à distance des sels de fer (plus de deux heures, si
possible).
Diminution de l'absorption digestive du strontium.
+ FLUOROQUINOLONES
Précaution d'emploi
Prendre le strontium à distance des fluoroquinolones (plus de deux
heures, si possible).
Diminution de l'absorption digestive du strontium.
227
+ ZINC
Précaution d'emploi
Prendre le strontium à distance des sels de zinc (plus de deux heures,
si possible).
Diminution de l'absorption digestive du strontium.
SUBSTANCES À ABSORPTION RÉDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET
ADSORBANTS
(acide acetylsalicylique, acide alendronique, acide clodronique, acide etidronique, acide ibandronique, acide oxidronique, acide pamidronique, acide risedronique,
acide tiludronique, acide zoledronique, alimemazine, atenolol, betamethasone, bictégravir, budesonide, chlorpromazine, chlortetracycline, cimetidine, ciprofloxacine,
clindamycine, cortisone, cyamemazine, demeclocycline, dexamethasone, digoxine, dolutégravir, doxycycline, elvitégravir, enoxacine, ethambutol, famotidine, fer,
fexofenadine, fluor, fluphenazine, isoniazide, lansoprazole, lédipasvir, levofloxacine, levomepromazine, levothyroxine, lincomycine, liothyronine sodique, lomefloxacine,
lymecycline, methylenecycline, methylprednisolone, metopimazine, metoprolol, minocycline, moxifloxacine, nizatidine, norfloxacine, ofloxacine, oxomemazine,
oxytetracycline, pefloxacine, penicillamine, phosphore, piperazine, pipotiazine, prednisolone, prednisone, proguanil, promethazine, propericiazine, propranolol,
raltégravir, ranitidine, rosuvastatine, roxadustat, sulpiride, tériflunomide, tetracycline, thyroxines, tigecycline, tiratricol, triamcinolone, ulipristal)
+ TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ADSORBANTS
ASDEC - PE
Association déconseillée:
- avec les inhibiteurs d'intégrase (raltégravir, bictégravir, dolutégravir,
cabotégravir)
Précaution d'emploi:
- avec les autres substances.
Par mesure de précaution, il convient de prendre ces topiques ou
antiacides à distance de tout autre médicament (plus de 2 heures, si
possible).
Diminution de l'absorption de ces substances.
SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Ce trouble du rythme cardiaque grave peut être provoqué par un certain nombre de médicaments, antiarythmiques ou non. L'hypokaliémie (cf. médicaments
hypokaliémiants) est un facteur favorisant, de même que la bradycardie (cf. médicaments bradycardisants) ou un allongement préexistant de l'intervalle QT, congénital
ou acquis.
Les médicaments à l’origine de cet effet indésirable sont notamment les antiarythmiques de classe Ia et III, et certains neuroleptiques. D'autres molécules
n’appartenant pas à ces classes sont également en cause.
Pour l’érythromycine et la vincamine, seules les formes administrées par voie intraveineuse sont concernées par cette interaction.
L'utilisation d'un médicament torsadogène avec un autre médicament torsadogène est contre-indiquée en règle générale.
Certains d’entre eux, en raison de leur caractère incontournable, font exception à la règle, en étant seulement déconseillés avec les autres torsadogènes. Il s’agit des
antiparasitaires (chloroquine, halofantrine, luméfantrine, pentamidine), de l'arsénieux, de l'hydroxychloroquine, de la méthadone, du crizotinib, du cotrimoxazole et des
neuroleptiques.
A noter que le citalopram, l’escitalopram, la dompéridone, l'hydroxyzine et la pipéraquine ne suivent pas cet assouplissement, et sont contre-indiqués avec tous les
torsadogènes, suite à un arbitrage européen.
(amiodarone, amisulpride, arsenieux, chloroquine, chlorpromazine, citalopram, cocaine, crizotinib, cyamemazine, disopyramide, domperidone, dronedarone,
droperidol, erythromycine, escitalopram, flupentixol, fluphenazine, halofantrine, haloperidol, hydroquinidine, hydroxychloroquine, hydroxyzine, levomepromazine,
lumefantrine, mequitazine, methadone, moxifloxacine, pentamidine, pimozide, pipamperone, pipéraquine, pipotiazine, quinidine, sotalol, spiramycine, sulpiride, tiapride,
toremifene, vandétanib, vincamine, zuclopenthixol)
+ ANAGRELIDE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ ANTIPARASITAIRES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication:
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine
et la pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si cela est possible, interrompre l'un des deux traitements. Si
l'association ne peut être évitée, contrôle préalable du QT et
surveillance ECG monitorée.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ ARSENIEUX
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaires, notamment de
torsades de pointes.
+ AZITHROMYCINE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
228
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Précaution d'emploi
Surveillance clinique et électrocardiographique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ BRADYCARDISANTS
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ CIPROFLOXACINE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ CLARITHROMYCINE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ CRIZOTINIB
Association DECONSEILLEE
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ DÉLAMANID
CI - ASDEC
Contre-indication:
- avec citalopram, dompéridone, escitalopram, hydroxyzine et
pipéraquine
Associations déconseillées
- avec les autres susbtances susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ GLASDÉGIB
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ HYDROXYCHLOROQUINE
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ HYPOKALIÉMIANTS
Précaution d'emploi
Corriger toute hypokaliémie avant d’administrer le produit et réaliser une
surveillance clinique, électrolytique et électrocardiographique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ LEVOFLOXACINE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ MÉDICAMENTS À L'ORIGINE D'UN HYPOGONADISME MASCULIN
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
229
+ METHADONE
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine
et la pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ NEUROLEPTIQUES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ NORFLOXACINE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant
l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ ONDANSETRON
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ ROXITHROMYCINE
Précaution d'emploi
Surveillance clinique et électrocardiographique pendant l'association.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ SULFAMÉTHOXAZOLE + TRIMÉTHOPRIME
Association DECONSEILLEE
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque de troubles ventriculaires, notamment de torsades de
pointes.
+ TORSADOGÈNES (SAUF ARSÉNIEUX, ANTIPARASITAIRES, NEUROLEPTIQUES, MÉTHADONE...)
CI - ASDEC
Contre-indication:
- Pour l'érythromycine et la vincamine, seules les formes administrées
par voie intraveineuse sont concernées par cette interaction.
- Pour la spiramycine, la voie IV et la voie orale sont concernées.
- Le citalopram, l'escitalopram, l'hydroxyzine, la dompéridone, la
pipéraquinei sont contre-indiqués quel que soit le torsadogène.
Association déconseillée:
- avec les antiparasitaires (chloroquine, halofantrine, luméfantrine,
pentamidine), les neuroleptiques, la méthadone, l'arsénieux et
l'hydroxychloroquine.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
SUBSTRATS À RISQUE DU CYP3A4
Ils sont principalement représentés par le rivaroxaban et l'apixaban, le ticagrélor, la simvastatine et l'atorvastatine, les immunosuppresseurs, le pimozide, la quétiapine,
le midazolam, les inhibiteurs de tyrosine kinase métabolisés, les vinca-alcaloïdes cytotoxiques, les taxanes, l'ergotamine, certains opiacés (alfentanil, sufentanil,
oxycodone), l'halofantrine et la luméfantrine, la quinine.
Pour connaître les risques et les niveaux de contrainte de chacun de ces substrats avec les inhibiteurs puissants du CYP3A4, il convient de se reporter aux
interactions spécifiques de chaque substrat.
(abémaciclib, alfentanil, apixaban, atorvastatine, axitinib, bortezomib, bosutinib, brigatinib, cabazitaxel, cabozantinib, céritinib, ciclosporine, cobimétinib, crizotinib,
dabrafénib, dasatinib, dihydroergotamine, docetaxel, ergotamine, erlotinib, everolimus, gefitinib, halofantrine, ibrutinib, imatinib, irinotecan, lapatinib, lorlatinib,
lumefantrine, midazolam, nilotinib, osimertinib, oxycodone, paclitaxel, palbociclib, pazopanib, pimozide, ponatinib, quetiapine, quinine, rivaroxaban, ruxolitinib,
simvastatine, sirolimus, sorafenib, sufentanil, sunitinib, tacrolimus, temsirolimus, ticagrelor, vandétanib, vinblastine, vincristine, vindesine, vinflunine, vinorelbine)
+ CRIZOTINIB
Association DECONSEILLEERisque de majoration de la toxicité de ces molécules par diminution
de leur métabolisme et/ou augmentation de leur biodisponibilité par
le crizotinib.
230
+ IDÉLALISIB
Association DECONSEILLEEAugmentation des concentrations plasmatiques du substrat par
diminution de son métabolisme hépatique par l’idelalisib.
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en compteMajoration des effets indésirables propres à chaque substrat, avec
conséquences souvent sévères.
SUCRALFATE
+ DIGOXINE
Précaution d'emploi
Prendre le sucralfate à distance de la digoxine (plus de 2 heures, si
possible).
Diminution de l'absorption digestive de la digoxine.
+ FLUOROQUINOLONES
Précaution d'emploi
Prendre le sucralfate à distance des fluoroquinolones (plus de 2 heures,
si possible).
Diminution de l'absorption digestive des fluoroquinolones.
+ HORMONES THYROÏDIENNES
Précaution d'emploi
Prendre les hormones thyroïdiennes à distance du sucralfate (plus de 2
heures, si possible).
Diminution de l'absorption digestive des hormones thyroïdiennes.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Prendre le sucralfate à distance de la phénytoïne (plus de 2 heures, si
possible).
Diminution de l'absorption digestive de la phénytoïne.
+ SULPIRIDE
Précaution d'emploi
Prendre le sucralfate à distance du sulpiride (plus de 2 heures, si
possible).
Diminution de l'absorption digestive du sulpiride.
SUFENTANIL
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier III - morphiniques - médicaments sédatifs - substrats à risque du CYP3A4
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de l’analgésique
opiacé en cas de traitement par un inhibiteur puissant du CYP3A4.
Augmentation de l’effet dépresseur respiratoire de l’analgésique
opiacé par diminution de son métabolisme hépatique.
SULFAFURAZOL
Voir aussi : médicaments méthémoglobinisants
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Association DECONSEILLEE
Utiliser de préférence une autre classe d'anti-infectieux, sinon
surveillance clinique étroite, dosage des concentrations de phénytoïne
et adaptation éventuelle de sa posologie pendant le traitement par le
sulfamide anti-infectieux et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
jusqu'à des valeurs toxiques (inhibition de son métabolisme).
SULFAMETHIZOL
Voir aussi : médicaments méthémoglobinisants - sulfamides antibactériens
+ METHENAMINE
Association DECONSEILLEEPrécipitation cristalline dans les voies urinaires (favorisée par
l'acidification des urines).
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Association DECONSEILLEE
Utiliser de préférence une autre classe d'anti-infectieux, sinon
surveillance clinique étroite, dosage des concentrations de phénytoïne
et adaptation éventuelle de sa posologie pendant le traitement par le
sulfamide anti-infectieux et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
jusqu'à des valeurs toxiques (inhibition de son métabolisme).
SULFAMETHOXAZOLE
Voir aussi : médicaments méthémoglobinisants - sulfamides antibactériens - sulfaméthoxazole + triméthoprime
+ ANTIVITAMINES K
Association DECONSEILLEE
Si l’association ne peut être évitée, contrôle plus fréquent de l’INR et
adaptation de la posologie de l’antivitamine K pendant le traitement par
cotrimoxazole et après son arrêt.
Augmentation importante de l’effet de l’antivitamine K et du risque
hémorragique.
231
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Association DECONSEILLEE
Utiliser de préférence une autre classe d'anti-infectieux, sinon
surveillance clinique étroite, dosage des concentrations de phénytoïne
et adaptation éventuelle de sa posologie pendant le traitement par le
sulfamide anti-infectieux et après son arrêt.
Augmentation des concentrations plasmatiques de phénytoïne
jusqu'à des valeurs toxiques (inhibition de son métabolisme).
SULFAMÉTHOXAZOLE + TRIMÉTHOPRIME
(sulfamethoxazole, trimethoprime)
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
Association DECONSEILLEE
Contre-indication :
- avec le citalopram, la dompéridone, l'escitalopram, l'hydroxyzine et la
pipéraquine.
Association déconseillée:
- avec les autres médicaments susceptibles de donner des torsades de
pointes.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque de troubles ventriculaires, notamment de torsades de
pointes.
+ SULFAMIDES HYPOGLYCÉMIANTS
A prendre en compteRares survenues d’hypoglycémies, notamment chez le sujet âgé,
dénutri ou insuffisant rénal.
SULFAMIDES ANTIBACTÉRIENS
(sulfadiazine, sulfadoxine, sulfamethizol, sulfamethoxazole)
+ METHOTREXATE
Précaution d'emploi
Dosage des concentrations de méthotrexate. Adapatation posologique
si nécessaire pendant l'association et après son arrêt.
Augmentation de la toxicité hématologique du méthotrexate.
SULFAMIDES HYPOGLYCÉMIANTS
(glibenclamide, gliclazide, glimepiride, glipizide)
+ ALCOOL (BOISSON OU EXCIPIENT)
Association DECONSEILLEE
Eviter la prise de boissons alcoolisées et de médicaments contenant de
l'alcool.
Effet antabuse, notamment pour glibenclamide, glipizide,
tolbutamide. Augmentation de la réaction hypoglycémique
(inhibition des réactions de compensation) pouvant faciliter la
survenue de coma hypoglycémique.
+ ANALOGUES DE LA SOMATOSTATINE
Précaution d'emploi
Renforcer l'autosurveillance glycémique et adapter si besoin la
posologie du sulfamide hypoglycemiant pendant le traitement par
l'analogue de la somatostatine.
Risque d'hypoglycémie ou d'hyperglycémie : diminution ou
augmentation des besoins en sulfamide hypoglycemiant, par
diminution ou augmentation de la sécrétion de glucagon endogène.
+ BÊTA-2 MIMÉTIQUES
Précaution d'emploi
Renforcer la surveillance sanguine et urinaire. Passer éventuellement à
l'insuline, le cas échéant.
Elévation de la glycémie par le bêta-2 mimétique.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Précaution d'emploi
Prévenir le patient et renforcer, surtout en début de traitement,
l'autosurveillance glycémique.
Tous les bêta-bloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Précaution d'emploi
Prévenir le malade et renforcer, surtout au début du traitement,
l'autosurveillance sanguine.
Tous les bêta-bloquants peuvent masquer certains symptômes de
l'hypoglycémie : palpitations et tachycardie.
+ CHLORPROMAZINE
Précaution d'emploi
Prévenir le patient et renforcer l'autosurveillance glycémique. Adapter
éventuellement la posologie du neuroleptique pendant le traitement et
après son arrêt.
A fortes posologies (100 mg par jour de chlorpromazine) : élévation
de la glycémie (diminution de la libération de l'insuline).
+ CLARITHROMYCINE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide hypoglycémiant pendant le
traitement par la clarithromycine.
Risque d'hypoglycémie par augmentation des concentrations
plasmatiques de l’antidiabétique.
232
+ DANAZOL
Association DECONSEILLEE
Si l'association ne peut être évitée, prévenir le patient et renforcer
l'autosurveillance glycémique. Adapter éventuellement la posologie de
l'antidiabétique pendant le traitement par le danazol et après son arrêt.
Effet diabétogène du danazol.
+ FLUCONAZOLE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide pendant le traitement par le
fluconazole.
Augmentation du temps de demi-vie du sulfamide avec survenue
possible de manifestations d'hypoglycémie.
+ INHIBITEURS DE L'ENZYME DE CONVERSION
Précaution d'emploi
Renforcer l'autosurveillance glycémique.
L'utilisation des IEC peut entraîner une majoration de l'effet
hypoglycémiant chez le diabétique traité par sulfamides
hypoglycémiants. La survenue de malaises hypoglycémiques
semble exceptionnelle (amélioration de la tolérance au glucose qui
aurait pour conséquence une réduction des besoins en sulfamides
hypoglycémiants).
+ MICONAZOLE
CONTRE-INDICATIONAugmentation de l'effet hypoglycémiant avec survenue possible de
manifestations hypoglycémiques, voire de coma.
+ SULFAMÉTHOXAZOLE + TRIMÉTHOPRIME
A prendre en compteRares survenues d’hypoglycémies, notamment chez le sujet âgé,
dénutri ou insuffisant rénal.
SULFASALAZINE
Voir aussi : dérivés de l'acide aminosalicylique (ASA)
+ DIGOXINE
Précaution d'emploi
Surveillance clinique, ECG et, éventuellement, de la digoxinémie. S'il y
a lieu, adaptation de la posologie de la digoxine pendant le traitement
par la sulfasalazine et après son arrêt.
Diminution de la digoxinémie pouvant atteindre 50 %.
+ PONATINIB
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque d’augmentation des concentrations plasmatiques de la
sulfasalazine par augmentation de son absorption intestinale par le
ponatinib.
+ TÉDIZOLIDE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de la
sulfasalazine, par augmentation de son absorption avec le
tédizolide administré par voie orale.
SULFINPYRAZONE
+ CICLOSPORINE
Précaution d'emploi
Contrôle des concentrations sanguines de ciclosporine et adaptation
éventuelle de sa posologie pendant le traitement par sulfinpyrazone et
après son arrêt.
Diminution des concentrations sanguines de ciclosporine par
augmentation de son métabolisme par la sulfinpyrazone.
SULPIRIDE
Voir aussi : médicaments sédatifs - médicaments à l'origine d'une hypotension orthostatique - neuroleptiques - neuroleptiques antipsychotiques (sauf clozapine) -
neuroleptiques susceptibles de donner des torsades de pointes - substances susceptibles de donner des torsades de pointes - substances à absorption réduite par les
topiques gastro-intestinaux, antiacides et adsorbants
+ SUCRALFATE
Précaution d'emploi
Prendre le sucralfate à distance du sulpiride (plus de 2 heures, si
possible).
Diminution de l'absorption digestive du sulpiride.
SULPROSTONE
+ MÉTHYLERGOMÉTRINE
CONTRE-INDICATION
Ne pas utiliser ces deux médicaments simultanément ou
successivement.
Risque de vasoconstriction coronaire pouvant être fatale.
233
SUNITINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés - substrats à risque du CYP3A4
+ GRAZOPREVIR + ELBASVIR
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Risque d’augmentation des effets indésirables du sunitinib par le
grazoprévir/elbasvir.
SUXAMETHONIUM
Voir aussi : curares
+ ANTICHOLINESTÉRASIQUES
A prendre en compteRisque d'allongement du bloc moteur, majoré en cas de déficit
partiel en pseudocholinestérase.
SYMPATHOMIMÉTIQUES ALPHA (VOIES ORALE ET/OU NASALE)
(etilefrine, midodrine, naphazoline, oxymetazoline, phenylephrine, synephrine, tetryzoline, tuaminoheptane)
+ ALCALOÏDES DE L'ERGOT DE SEIGLE DOPAMINERGIQUES
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ IMAO IRRÉVERSIBLES
Association DECONSEILLEECrises hypertensives (inhibition du métabolisme des amines
pressives). Du fait de la durée d'action de l'IMAO, cette interaction
est encore possible 15 jours après l'arrêt de l'IMAO.
+ SYMPATHOMIMÉTIQUES INDIRECTS
CONTRE-INDICATIONRisque de vasoconstriction et/ou de poussées hypertensives.
SYMPATHOMIMÉTIQUES ALPHA ET BÊTA (VOIE IM ET IV)
(adrenaline, dopamine, noradrenaline, norepinephrine)
+ ANESTHÉSIQUES VOLATILS HALOGÉNÉS
A prendre en compteDécrit avec l'halothane et le cyclopropane.
Troubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ ANTIDÉPRESSEURS IMIPRAMINIQUES
Association DECONSEILLEEHypertension paroxystique avec possibilité de troubles du rythme
(inhibition de l'entrée du sympathomimétique dans la fibre
sympathique).
+ IMAO IRRÉVERSIBLES
Précaution d'emploi
A n'utiliser que sous contrôle médical strict.
Augmentation de l'action pressive du sympathomimétique, le plus
souvent modérée.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
Précaution d'emploi
A n'utiliser que sous contrôle médical strict.
Par extrapolation à partir des IMAO non sélectifs : risque
d'augmentation de l'action pressive.
+ MÉDICAMENTS MIXTES ADRÉNERGIQUES-SÉROTONINERGIQUES
Association DECONSEILLEEHypertension paroxystique avec possibilité de troubles du rythme
(inhibition de l'entrée du sympathomimétique dans la fibre
sympathique).
SYMPATHOMIMÉTIQUES INDIRECTS
(bupropion, cafedrine, ephedrine, methylphenidate, pseudoephedrine, theodrenaline)
+ AUTRES SYMPATHOMIMETIQUES INDIRECTS
CONTRE-INDICATIONRisque de vasoconstriction et/ou de crises hypertensives.
234
+ ALCALOÏDES DE L'ERGOT DE SEIGLE DOPAMINERGIQUES
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
Association DECONSEILLEERisque de vasoconstriction et/ou de poussées hypertensives.
+ ANESTHÉSIQUES VOLATILS HALOGÉNÉS
Précaution d'emploi
En cas d'intervention programmée, il est préférable d'interrompre le
traitement quelques jours avant l'intervention.
Poussée hypertensive peropératoire.
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONHypertension paroxystique, hyperthermie pouvant être fatale. Du
fait de la durée d'action de l'IMAO, cette interaction est encore
possible 15 jours après l'arrêt de l'IMAO.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
CI - ASDEC
Contre-indication :
avec le bupropion
Association déconseillée :
avec les autres sympathomimétiques indirects
Risque de vasoconstriction et/ou de poussées hypertensives.
+ SYMPATHOMIMÉTIQUES ALPHA (VOIES ORALE ET/OU NASALE)
CONTRE-INDICATIONRisque de vasoconstriction et/ou de poussées hypertensives.
TACROLIMUS
Voir aussi : hyperkaliémiants - immunosuppresseurs - médicaments néphrotoxiques - substrats à risque du CYP3A4
+ AMINOSIDES
A prendre en compteAugmentation de la créatininémie plus importante que sous
tacrolimus seul (synergie des effets néphrotoxiques des deux
substances).
+ AMIODARONE
Précaution d'emploi
Dosage des concentrations sanguines de tacrolimus, contrôle de la
fonction rénale et adaptation de la posologie de tacrolimus pendant
l’association et à l’arrêt de l’amiodarone.
Augmentation des concentrations sanguines de tacrolimus par
inhibition de son métabolisme par l’amiodarone.
+ AMPHOTERICINE B
A prendre en compteAvec l'amphotéricine B administrée par voie IV : augmentation de
la créatininémie plus importante que sous tacrolimus seul (synergie
des effets néphrotoxiques des deux substances).
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Précaution d'emploi
Surveiller la fonction rénale en début de traitement par l’AINS.
Risque d’addition des effets néphrotoxiques, notamment chez le
sujet âgé.
+ CLINDAMYCINE
Précaution d'emploi
Contrôle renforcé des dosages sanguins de tacrolimus et augmentation
éventuelle de sa posologie.
Diminution des concentrations sanguines de l'immunosuppresseur,
avec risque de perte de l'activité immunosuppressive.
+ DABIGATRAN
Association DECONSEILLEERisque d'augmentation des concentrations plasmatiques de
dabigatran.
+ DANAZOL
Précaution d'emploi
Dosage des concentrations sanguines du tacrolimus et adaptation de sa
posologie pendant l'association et après son arrêt, avec contrôle de la
fonction rénale.
Augmentation des concentrations sanguines du tacrolimus par
inhibition de son métabolisme hépatique.
+ DIURÉTIQUES ÉPARGNEURS DE POTASSIUM (SEULS OU ASSOCIÉS)
Association DECONSEILLEEHyperkaliémie potentiellement létale, surtout lors d'une insuffisance
rénale (addition des effets hyperkaliémiants).
235
+ GRAZOPREVIR + ELBASVIR
Précaution d'emploi
Surveillance clinique et biologique étroite.
Augmentation des concentrations plasmatiques de tacrolimus par
inhibition de son métabolisme hépatique.
+ JOSAMYCINE
Association DECONSEILLEEAugmentation des concentrations sanguines de tacrolimus et de la
créatininémie, par inhibition du métabolisme hépatique du
tacrolimus par la josamycine.
+ LANSOPRAZOLE
Précaution d'emploi
Dosage des concentrations sanguines du tacrolimus, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après son arrêt.
Augmentation des concentrations sanguines du tacrolimus.
+ MIFAMURTIDE
CONTRE-INDICATIONRisque d'atteinte des macrophages spléniques et des cellules
phagocytaires mononuclées.
+ OMBITASVIR + PARITAPRÉVIR
Association DECONSEILLEE
Si l’association s’avère nécessaire, contrôle strict de la fonction rénale,
dosage des concentrations sanguines de l'immunosuppresseur et
adaptation éventuelle de la posologie.
En association avec le ritonavir : augmentation significative des
concentrations de l’immunosuppresseur avec risque de majoration
de sa toxicité par la bithérapie.
+ OMEPRAZOLE
Précaution d'emploi
Dosage des concentrations sanguines du tacrolimus, contrôle de la
fonction rénale et adaptation de la posologie pendant l'association et
après son arrêt.
Augmentation des concentrations sanguines du tacrolimus.
+ POTASSIUM
Association DECONSEILLEE
Sauf en cas d'hypokaliémie.
Pour une quantité de potassium > à 1 mmol/prise, hyperkaliémie
potentiellement létale, notamment chez l'insuffisant rénale (addition
des effets hyperkaliémiants).
+ TIGECYCLINE
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant le
traitement par la tigécycline.
Augmentation des concentrations sanguines de
l’immunosuppresseur, avec risque d'effets néphrotoxiques.
+ VERAPAMIL
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines du tacrolimus
(diminution de son métabolisme hépatique par le verapamil).
TALAZOPARIB
+ AMIODARONE
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ CICLOSPORINE
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ CLARITHROMYCINE
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ DRONEDARONE
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ ERYTHROMYCINE
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
236
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ ITRACONAZOLE
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ QUINIDINE
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ VERAPAMIL
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
TAMOXIFENE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K.
Risque d'augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
+ BUPROPION
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par le bupropion.
+ DULOXETINE
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par la duloxétine.
+ FLUOXETINE
Association DECONSEILLEEBaisse de l’efficacité du tamoxifène, par inhibition de la formation
de son métabolite actif par la fluoxétine.
+ INDUCTEURS ENZYMATIQUES
A prendre en compteRisque d’inefficacité du tamoxifène par augmentation de son
métabolisme par l’inducteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque d’inefficacité du tamoxifène par augmentation de son
métabolisme par le millepertuis.
+ PAROXETINE
Association DECONSEILLEEBaisse de l’efficacité du tamoxifène, par inhibition de la formation
de son métabolite actif par la paroxétine.
+ QUINIDINE
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par la quinidine.
+ ROLAPITANT
Association DECONSEILLEERisque de baisse de l’efficacité du tamoxifène par inhibition de la
formation de son métabollite actif par le rolapitant.
+ TERBINAFINE
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par la terbinafine.
237
TAMSULOSINE
Voir aussi : alphabloquants à visée urologique - médicaments abaissant la pression artérielle - médicaments à l'origine d'une hypotension orthostatique
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la tamsulosine
pendant le traitement par l’inhibiteur enzymatique et après son arrêt, le
cas échéant.
Risque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
+ DILTIAZEM
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la tamsulosine
pensant le traitement par l’inhibiteur enzymatique et après son arrêt, le
cas échéant.
Risque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEERisque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la tamsulosine
pensant le traitement par l’inhibiteur enzymatique et après son arrêt, le
cas échéant.
Risque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
TÉDIZOLIDE
Voir aussi : IMAO-A réversibles, y compris oxazolidinones et bleu de méthylène
+ IMATINIB
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de
l'imatinib, par augmentation de son absorption avec le tédizolide
administré par voie orale.
+ LAPATINIB
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
lapatinib, par augmentation de son absorption avec le tédizolide
administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
+ METHOTREXATE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
méthotrexate, par augmentation de son absorption avec le
tédizolide administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
+ ROSUVASTATINE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de la
rosuvastatine, par augmentation de son absorption avec le
tédizolide administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
+ SULFASALAZINE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques de la
sulfasalazine, par augmentation de son absorption avec le
tédizolide administré par voie orale.
+ TOPOTECANE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
topotécan, par augmentation de son absorption avec le tédizolide
administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
TELBIVUDINE
+ PEG-INTERFERON ALFA-2A
CONTRE-INDICATIONRisque majoré de neuropathies périphériques.
TELITHROMYCINE
Voir aussi : inhibiteurs puissants du CYP3A4 - macrolides (sauf spiramycine)
+ ATORVASTATINE
CONTRE-INDICATIONRisque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
238
+ DIGOXINE
Précaution d'emploi
Surveillance clinique et éventuellement de la digoxinémie pendant le
traitement par la télithromycine et après son arrêt.
Augmentation de la digoxinémie par augmentation de son
absorption.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEE
En cas d’association, contrôle strict de la fonction rénale, dosage des
concentrations sanguines de l'immunosuppresseur et adaptation
éventuelle de la posologie.
Augmentation très importante des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution des concentrations plasmatiques de la télithromycine,
avec risque d'échec du traitement anti-infectieux, par augmentation
de son métabolisme hépatique par l'inducteur.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATION
chez le patient insuffisant rénal ou hépatique sévère.
Risque de majoration des effets indésirables, notamment à type de
troubles du rythme cardiaque.
+ MILLEPERTUIS
Association DECONSEILLEEDiminution des concentrations plasmatiques de la télithromycine,
avec risque d'échec du traitement anti-infectieux, par augmentation
du métabolisme hépatique de la télithromycine par le millepertuis.
+ RIFAMPICINE
Association DECONSEILLEEDiminution très importante des concentrations plasmatiques de la
télithromycine, avec risque d'échec du traitement anti-infectieux,
par augmentation du métabolisme hépatique de la télithromycine
par la rifampicine.
+ VENLAFAXINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
TEMSIROLIMUS
Voir aussi : immunosuppresseurs - médicaments, bradykinine et angio-œdème - substrats à risque du CYP3A4
+ INHIBITEURS DE L'ENZYME DE CONVERSION
A prendre en compteMajoration du risque d’angio-oedème.
TENOFOVIR ALAFÉNAMIDE
+ P A S SODIQUE
A prendre en compteDiminution des deux tiers de l’exposition du ténofovir avec une
formulation de PAS calcique.
TÉNOFOVIR ALAFÉNAMIDE
+ CICLOSPORINE
Précaution d'emploi
En cas de co-administration avec la ciclosporine, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ COBICISTAT
Précaution d'emploi
En cas de co-administration, la dose de ténofovir alafénamide doit être
limitée à 10 mg par jour. L’association avec les autres inhibiteurs de
protéases du VIH n’a pas été étudiée.
Avec l'atazanavir, le darunavir ou le lopinavir boostés par cobicistat,
augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique pendant
l’association et 1 à 2 semaines après l’arrêt de l’inducteur.
Diminution des concentrations plasmatiques du ténofovir
alafénamide par diminution de son absorption par l’inducteur.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
En cas de co-administration, la dose de ténofovir alafénamide doit être
limitée à 10 mg par jour. L’association avec les autres inhibiteurs de
protéases du VIH n’a pas été étudiée.
Avec l'atazanavir, le darunavir ou le lopinavir, augmentation des
concentrations plasmatiques du ténofovir alafénamide par
augmentation de son absorption.
239
+ ITRACONAZOLE
Précaution d'emploi
En cas de co-administration avec l’itraconazole, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ KETOCONAZOLE
Précaution d'emploi
En cas de co-administration avec le kétoconazole, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ RIFAMPICINE
Association DECONSEILLEE
Surveillance clinique pendant l’association et 1 à 2 semaines après
l’arrêt de la rifampicine.
Diminution des concentrations plasmatiques du ténofovir
alafénamide par diminution de son absorption par la rifampicine.
+ VERAPAMIL
Précaution d'emploi
En cas de co-administration avec le vérapamil, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
TENOFOVIR DISOPROXIL
Voir aussi : médicaments néphrotoxiques
+ ANTI-INFLAMMATOIRES NON STÉROÏDIENS
Précaution d'emploi
En cas d’association, surveiller la fonction rénale.
Risque de majoration de la néphrotoxicité du ténofovir, notamment
avec des doses élevées de l'anti-inflammatoire ou en présence de
facteurs de risque d'insuffisance rénale.
+ ATAZANAVIR
A prendre en compte
Ne pas administrer l’atazanavir avec le ténofovir sans ritonavir.
Diminution d’environ un tiers de l’exposition à l’atazanavir chez le
patient en cas d’association au ténofovir, comparativement au sujet
sain recevant la même association.
+ DIDANOSINE
Association DECONSEILLEERisque d'échec du traitement antirétroviral, voire émergence de
résistances. De plus, majoration du risque de la toxicité
mitochondriale de la didanosine.
+ LÉDIPASVIR
Précaution d'emploi
Surveillance clinique et biologique, notamment de la fonction rénale.
Lors de sa co-administration avec un inhibiteur de protéase,
augmentation des concentrations plasmatiques du ténofovir par le
lédipasvir.
+ P A S SODIQUE
A prendre en compteDiminution des deux tiers de l’exposition du ténofovir avec une
formulation de PAS calcique.
TERBINAFINE
+ CICLOSPORINE
Précaution d'emploi
Contrôle des concentrations sanguines de ciclosporine et adaptation
éventuelle de sa posologie pendant le traitement par terbinafine et
après son arrêt.
Diminution des concentrations sanguines de ciclosporine.
+ CODEINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ MEQUITAZINE
Association DECONSEILLEERisque de majoration des effets indésirables de la méquitazine, par
inhibition de son métabolisme par l’inhibiteur enzymatique.
+ METOPROLOL
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie du
métoprolol pendant le traitement par la terbinafine.
Chez l'insuffisant cardiaque, risque d'augmentation des effets
indésirables du métoprolol, par diminution de son métabolisme
hépatique par la terbinafine.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
propafénone pendant le traitement par la terbinafine.
Risque d'augmentation des effets indésirables de la propafénone,
par diminution de son métabolisme hépatique par la terbinafine.
240
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique. Si besoin, adaptation de la posologie de la
terbinafine pendant le traitement par la rifampicine.
Diminution des concentrations plasmatiques et de l'efficacité de la
terbinafine, par augmentation de son métabolisme hépatique par la
rifampicine.
+ TAMOXIFENE
Association DECONSEILLEERisque de baisse de l'efficacité du tamoxifène, par inhibition de la
formation de son métabolite actif par la terbinafine.
+ TETRABENAZINE
CONTRE-INDICATIONAugmentation, possiblement très importante, de l’exposition des
métabolites actifs de la tétrabénazine.
+ TRAMADOL
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
TÉRIFLUNOMIDE
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ SELEXIPAG
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
+ VACCINS VIVANTS ATTÉNUÉS
Association DECONSEILLEERisque de maladie vaccinale généralisée, éventuellement mortelle.
TETRABENAZINE
Voir aussi : médicaments sédatifs
+ BUPROPION
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ CINACALCET
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ DOPAMINERGIQUES
Association DECONSEILLEEAntagonisme réciproque entre le dopaminergique et la
tétrabénazine.
+ DULOXETINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ FLUOXETINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONRisque de crises hypertensives. Du fait de la durée d'action de
l'IMAO, cette interaction est encore théoriquement possible 15 jours
après son arrêt.
+ LEVODOPA
Association DECONSEILLEEAntagonisme réciproque entre la lévodopa et la tétrabénazine.
+ PAROXETINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
241
+ QUINIDINE
CONTRE-INDICATIONAugmentation possiblement très importante de l’exposition des
métabolites actifs de la tétrabénazine.
+ TERBINAFINE
CONTRE-INDICATIONAugmentation, possiblement très importante, de l’exposition des
métabolites actifs de la tétrabénazine.
THALIDOMIDE
Voir aussi : bradycardisants - médicaments sédatifs
+ DIDANOSINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
+ STAVUDINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque majoré de survenue de neuropathies périphériques par
addition d'effets indésirables.
THEOPHYLLINE
Voir aussi : médicaments à risque lors du sevrage tabagique - théophylline (et, par extrapolation, aminophylline)
+ GIVOSIRAN
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Risque d’augmentation de la théophyllinémie avec signes de
surdosage par diminution de son métabolisme hépatique.
+ LITHIUM
Précaution d'emploi
Surveillance stricte de la lithémie et adaptation éventuelle de la
posologie du lithium.
Diminution de la lithémie avec risque de baisse de l’efficacité
thérapeutique.
+ PROPAFENONE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Risque d’augmentation de la théophyllinémie par diminution de son
métabolisme hépatique par la propafénone.
+ VÉMURAFÉNIB
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la théophylline
pendant le traitement par vémurafénib et après son arrêt.
Augmentation importante des concentrations de théophylline, avec
risques de majoration de ses effets indésirables.
THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
(aminophylline, theophylline)
+ CIMETIDINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie. S'il y a
lieu, adaptation de la théophylline pendant le traitement par la
cimétidine et après son arrêt.
Avec la cimétidine utilisée à des doses supérieures ou égales à
800 mg/j : augmentation de la théophyllinémie avec risque de
surdosage (diminution du métabolisme de la théophylline).
+ CIPROFLOXACINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Augmentation de la théophyllinémie avec risque de surdosage, par
diminution de son métabolisme hépatique par la ciprofloxacine.
+ CLARITHROMYCINE
A prendre en compteRisque d'augmentation de la théophyllinémie, particulièrement chez
l'enfant.
+ DIPYRIDAMOLE
Précaution d'emploi
Interrompre un traitement par théophylline au moins 5 jours avant une
imagerie myocardique avec le dipyridamole.
Avec le dipyridamole par voie injectable : réduction de l’effet
vasodilatateur du dipyridamole par la théophylline.
+ ENOXACINE
CONTRE-INDICATIONSurdosage en théophylline par diminution importante de son
métabolisme.
242
+ ERYTHROMYCINE
Association DECONSEILLEESurdosage en théophylline par diminution de son élimination
hépatique, plus particulièrement à risque chez l'enfant.
+ FLUCONAZOLE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par le fluconazole et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution de la clairance de la théophylline).
+ FLUVOXAMINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; si
besoin, adaptation de la posologie de la théophylline pendant le
traitement par la fluvoxamine et après son arrêt.
Augmentation de la théophyllinémie avec signes de surdosage
(diminution du métabolisme hépatique de la théophylline).
+ HALOTHANE
Association DECONSEILLEETroubles du rythme ventriculaire graves par augmentation de
l'excitabilité cardiaque.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Surveillance clinique et, si besoin, de la théophyllinémie. Adaptation
éventuelle de la posologie de la théophylline pendant le traitement par
l'inducteur et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
théophylline par augmentation de son métabolisme hépatique par
l'inducteur.
+ INHIBITEURS DE LA XANTHINE OXYDASE
Précaution d'emploi
Surveillance clinique et contrôle de la théophyllinémie jusqu'à deux à
trois semaines après la mise en route du traitement par l'inhibiteur ; s'il y
a lieu, adaptation de la posologie pendant le traitement par l'association.
En cas de posologies élevées de l'inhibiteur, augmentation des
concentrations plasmatiques de théophylline par inhibition de son
métabolisme.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par l'inhibiteur de protéases et après son arrêt.
Diminution des concentrations plasmatiques de la théophylline, par
augmentation de son métabolisme hépatique.
+ JOSAMYCINE
A prendre en compteRisque d'augmentation de la théophyllinémie, particulièrement chez
l'enfant.
+ MEXILETINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par la mexilétine et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution du métabolisme hépatique de la théophylline).
+ MILLEPERTUIS
CONTRE-INDICATION
En cas d'association fortuite, ne pas interrompre brutalement la prise de
millepertuis mais contrôler les concentrations plasmatiques (ou
l'efficacité) du médicament associé avant puis après l'arrêt du
millepertuis.
Diminution des concentrations plasmatiques de la théophylline, en
raison de l'effet inducteur enzymatique du millepertuis, avec risque
de baisse d'efficacité voire d'annulation de l'effet dont les
conséquences peuvent être éventuellement graves (survenue d'un
trouble ventilatoire obstructif).
+ NORFLOXACINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution du métabolisme de la théophylline).
+ PEFLOXACINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution du métabolisme de la théophylline).
+ PENTOXIFYLLINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par la pentoxifylline et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(compétition au niveau du métabolisme hépatique de la
théophylline).
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et, si besoin, de la théophyllinémie. Adapter, s'il y
a lieu, la posologie de la théophylline pendant le traitement par la
rifampicine et après son arrêt.
Diminution des concentrations plasmatiques et de l'efficacité de la
théophylline (augmentation de son métabolisme par induction
enzymatique).
243
+ ROXITHROMYCINE
A prendre en compteRisque d'augmentation de la théophyllinémie, particulièrement chez
l'enfant.
+ STIRIPENTOL
Précaution d'emploi
Surveillance clinique, dosage plasmatique et adaptation éventuelle de la
posologie de théophylline.
Augmentation possible de la théophyllinémie, avec risque de
surdosage, par inhibition de son métabolisme hépatique.
+ TIABENDAZOLE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
(et après son arrêt, dans le cas où l'anthelminthique est prescrit pour
une durée excédant 48 heures).
Augmentation de la théophyllinémie avec risque de surdosage, par
diminution du métabolisme hépatique de la théophylline.
+ TICLOPIDINE
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par la ticlopidine et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution de la clairance plasmatique de la théophylline).
THROMBOLYTIQUES
(alteplase recombinante, reteplase, streptokinase, tenecteplase, urokinase)
+ ANTIAGRÉGANTS PLAQUETTAIRES
A prendre en compteAugmentation du risque hémorragique.
+ ANTICOAGULANTS ORAUX
A prendre en compteAugmentation du risque hémorragique.
+ DÉFIBROTIDE
CONTRE-INDICATIONRisque hémorragique accru.
+ HÉPARINES (DOSES CURATIVES ET/OU SUJET ÂGÉ)
A prendre en compteAugmentation du risque hémorragique.
TIABENDAZOLE
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
(et après son arrêt, dans le cas où l'anthelminthique est prescrit pour
une durée excédant 48 heures).
Augmentation de la théophyllinémie avec risque de surdosage, par
diminution du métabolisme hépatique de la théophylline.
TIAGABINE
Voir aussi : anticonvulsivants métabolisés
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Une augmentation de la posologie de tiagabine peut s'avérer
nécessaire en cas d'association à un anticonvulsivant inducteur
enzymatique.
Diminution des concentrations plasmatiques de la tiagabine par
augmentation de son métabolisme hépatique par l'inducteur.
+ RIFAMPICINE
Précaution d'emploi
Une augmentation de la posologie de la tiagabine peut s’avérer
nécessaire en cas d’association à la rifampicine.
Diminution des concentrations plasmatiques de la tiagabine par
augmentation de son métabolisme hépatique.
TIANEPTINE
+ IMAO IRRÉVERSIBLES
Association DECONSEILLEERisque de collapsus, hypertension paroxystique, hyperthermie,
convulsions, décès.
244
TIBOLONE
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par la tibolone et après son
arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique.
TICAGRELOR
Voir aussi : antiagrégants plaquettaires - substrats à risque du CYP3A4
+ ACIDE ACETYLSALICYLIQUE
ASDEC - PE
Association déconseillée :
- en dehors des indications validées pour cette association dans les
syndromes coronariens aigus.
Précaution d'emploi :
- dans les indications validées pour cette association dans les
syndromes coronariens aigus. Surveillance clinique.
Majoration du risque hémorragique par addition des activités
antiagrégantes plaquettaires.
+ DABIGATRAN
A prendre en compteAugmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
+ DILTIAZEM
A prendre en compteRisque d’augmentation des concentrations plasmatiques de
ticagrelor par diminution de son métabolisme hépatique.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution importante des concentrations plasmatiques de
ticagrelor par augmentation de son métabolisme hépatique par
l'inducteur enzymatique, avec risque de diminution de l’effet
thérapeutique.
+ INHIBITEURS PUISSANTS DU CYP3A4
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de ticagrelor par
diminution de son métabolisme hépatique par l’inhibiteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution importante des concentrations plasmatiques
de ticagrelor par augmentation de son métabolisme hépatique par
le millepertuis, avec diminution de son effet thérapeutique.
+ OMBITASVIR + PARITAPRÉVIR
CONTRE-INDICATIONAugmentation des concentrations plasmatiques du ticagrélor par
diminution de son métabolisme hépatique par la bithérapie.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEDoublement des concentrations plasmatiques de l'antiagrégant,
avec risque de majoration des effets indésirables, notamment
hémorragiques.
+ RIFAMPICINE
Association DECONSEILLEEDiminution importante des concentrations plasmatiques de
ticagrelor par augmentation de son métabolisme hépatique par la
rifampicine, avec risque de diminution de l’effet thérapeutique.
+ VERAPAMIL
A prendre en compteRisque d’augmentation des concentrations plasmatiques de
ticagrelor par diminution de son métabolisme hépatique.
TICLOPIDINE
Voir aussi : antiagrégants plaquettaires
+ ACIDE ACETYLSALICYLIQUE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite.
Majoration du risque hémorragique par addition des activités
antiagrégantes plaquettaires.
245
+ CICLOSPORINE
Précaution d'emploi
Augmentation de la posologie de la ciclosporine sous contrôle des
concentrations sanguines. Réduction de la posologie en cas d'arrêt de
la ticlopidine.
Diminution des concentrations sanguines de ciclosporine.
+ KETAMINE
A prendre en compteAugmentation des concentrations plasmatiques de kétamine par
diminution de son métabolisme par la ticlopidine.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et contrôle des concentrations plasmatiques de
phénytoïne.
Augmentation des concentrations plasmatiques de phénytoïne
avec signes de surdosage (inhibition du métabolisme de la
+ THÉOPHYLLINE (ET, PAR EXTRAPOLATION, AMINOPHYLLINE)
Précaution d'emploi
Surveillance clinique et éventuellement de la théophyllinémie ; s'il y a
lieu, adaptation de la posologie de la théophylline pendant le traitement
par la ticlopidine et après son arrêt.
Augmentation de la théophyllinémie avec risque de surdosage
(diminution de la clairance plasmatique de la théophylline).
TIGECYCLINE
Voir aussi : cyclines - substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant le
traitement par la tigécycline.
Augmentation des concentrations sanguines de
l’immunosuppresseur, avec risque d'effets néphrotoxiques.
+ TACROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant le
traitement par la tigécycline.
Augmentation des concentrations sanguines de
l’immunosuppresseur, avec risque d'effets néphrotoxiques.
TOLVAPTAN
+ AMIODARONE
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
+ DILTIAZEM
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
+ FLUCONAZOLE
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Réduire la posologie des deux tiers aux trois quarts, selon la dose
prescrite.
Augmentation importante (entre 2 à 5 fois en moyenne) des
concentrations de tolvaptan, avec risque de majoration importante
des effets indésirables, notamment diurèse importante,
déshydratation, insuffisance rénale aiguë.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation importante (entre 2 à 5 fois en moyenne) des
concentrations de tolvaptan, avec risque de majoration importante
des effets indésirables, notamment diurèse importante,
déshydratation, insuffisance rénale aiguë.
+ VERAPAMIL
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
246
TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET ADSORBANTS
Les topiques gastro-intestinaux, le charbon, le lanthane et les antiacides (sels d'aluminium, de calcium et de magnésium), associés ou non aux alginates, diminuent la
résorption digestive de certains autres médicaments ingérés simultanément.
Par mesure de précaution, il convient de prendre ces topiques ou antiacides à distance de tout autre médicament (plus de 2 heures, si possible).
(charbon active, charbon vegetal officinal, crospovidone, diosmectite, gel d'hydroxyde d'aluminium et de carbonate de magnesium codesseches, hydrotalcite, kaolin
lourd, lanthane, magaldrate, magnesium (hydroxyde de), magnesium (trisilicate de), monmectite)
+ MÉDICAMENTS ADMINISTRÉS PAR VOIE ORALE
ASDEC - PE
Prendre les topiques ou antiacides, adsorbants à distance de ces
substances (plus de 2 heures, si possible).
Diminution de l'absorption de certains autres médicaments ingérés
simultanément.
+ POLYSTYRÈNE SULFONATE DE CALCIUM
Précaution d'emploi
Comme avec tout médicament oral pris avec l’un ou l’autre de ces
médicaments, respecter un intervalle entre les prises (plus de 2 heures,
si possible).
Risque d'alcalose métabolique chez l'insuffisant rénal
+ POLYSTYRÈNE SULFONATE DE SODIUM
Précaution d'emploi
Comme avec tout médicament oral pris avec l’un ou l’autre de ces
médicaments, respecter un intervalle entre les prises (plus de 2 heures,
si possible).
Risque d'alcalose métabolique chez l'insuffisant rénal.
+ SUBSTANCES À ABSORPTION RÉDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET
ADSORBANTS
ASDEC - PE
Association déconseillée:
- avec les inhibiteurs d'intégrase (raltégravir, bictégravir, dolutégravir,
cabotégravir)
Précaution d'emploi:
- avec les autres substances.
Par mesure de précaution, il convient de prendre ces topiques ou
antiacides à distance de tout autre médicament (plus de 2 heures, si
possible).
Diminution de l'absorption de ces substances.
TOPIRAMATE
Voir aussi : anticonvulsivants métabolisés
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique du
topiramate pendant le traitement par la carbamazépine et après son
arrêt.
Diminution des concentrations du topiramate avec risque de
moindre efficacité, par augmentation de son métabolisme
hépatique par la carbamazépine.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
Si l’association s’avère nécessaire, utiliser une méthode additionnel de
type mécanique pendant la durée de l’association et un cycle suivant
l’arrêt du topiramate.
Pour des doses de topiramate >= 200 mg/jour :
Risque de diminution de l’efficacité contraceptive par diminution
des concentrations en estrogène.
+ LITHIUM
Précaution d'emploi
Surveillance clinique et biologique. Adaptation de la posologie du lithium.
Pour des doses de topiramate >= 200 mg par jour : augmentation
de la lithémie pouvant atteindre des valeurs toxiques, avec signes
de surdosage en lithium.
+ OXCARBAZEPINE
Précaution d'emploi
Surveillance clinique, et si besoin, adaptation posologique du
topiramate pendant le traitement par l'oxcarbazépine et après son arrêt.
Risque de diminution des concentrations du topiramate avec risque
de moindre efficacité, par augmentation de son métabolisme
hépatique par l'oxcarbazépine.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
TOPOTECANE
Voir aussi : cytotoxiques
+ TÉDIZOLIDE
Association DECONSEILLEERisque d’augmentation des concentrations plasmatiques du
topotécan, par augmentation de son absorption avec le tédizolide
administré par voie orale, ou par diminution de son
élimination avec le tédizolide administré par voie IV.
247
TORSADOGÈNES (SAUF ARSÉNIEUX, ANTIPARASITAIRES, NEUROLEPTIQUES, MÉTHADONE...)
(amiodarone, citalopram, cocaine, disopyramide, domperidone, dronedarone, erythromycine, escitalopram, hydroquinidine, hydroxyzine, mequitazine, moxifloxacine,
pipéraquine, quinidine, sotalol, spiramycine, toremifene, vandétanib, vincamine)
+ SUBSTANCES SUSCEPTIBLES DE DONNER DES TORSADES DE POINTES
CI - ASDEC
Contre-indication:
- Pour l'érythromycine et la vincamine, seules les formes administrées
par voie intraveineuse sont concernées par cette interaction.
- Pour la spiramycine, la voie IV et la voie orale sont concernées.
- Le citalopram, l'escitalopram, l'hydroxyzine, la dompéridone, la
pipéraquinei sont contre-indiqués quel que soit le torsadogène.
Association déconseillée:
- avec les antiparasitaires (chloroquine, halofantrine, luméfantrine,
pentamidine), les neuroleptiques, la méthadone, l'arsénieux et
l'hydroxychloroquine.
Si l’association ne peut être évitée, contrôle clinique et
électrocardiographique régulier.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
TRABECTÉDINE
+ ITRACONAZOLE
Association DECONSEILLEE
Si l’association est nécessaire, surveillance clinique et adaptation
éventuelle de la posologie de la trabectedine pendant la durée du
traitement par l’itraconazole.
Risque d’augmentation des concentrations plasmatiques de la
trabectedine par l’itraconazole.
TRAITEMENTS DE SUBSTITUTION NICOTINIQUE
(nicotine
+ MÉDICAMENTS À RISQUE LORS DU SEVRAGE TABAGIQUE
A prendre en compteRisque de surdosage lors du remplacement du tabac par le
traitement substitutif.
TRAMADOL
Voir aussi : analgésiques morphiniques agonistes - analgésiques morphiniques de palier II - morphiniques - médicaments abaissant le seuil épileptogène -
médicaments sédatifs - médicaments à l'origine d'un syndrome sérotoninergique
+ ANTICOAGULANTS ORAUX
A prendre en compte
Surveillance particulièrement chez le sujet âgé.
Augmentation du risque hémorragique
+ BUPROPION
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ CINACALCET
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ DULOXETINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ FLUOXETINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONRisque d'apparition d'un syndrome sérotoninergique : diarrhée,
sueurs, tremblements, confusion, voire coma.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
Association DECONSEILLEERisque d'apparition d'un syndrome sérotoninergique : diarrhée,
tachycardie, sueurs, tremblements, confusion voire coma.
+ IMAO-B
A prendre en compteRisque d’apparition d’un syndrome sérotoninergique.
248
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteRisque d'apparition de convulsions et/ou d'un syndrome
sérotoninergique.
+ ONDANSETRON
A prendre en compteDiminution de l’intensité et de la durée de l’effet analgésique du
tramadol et risque de diminution de l’effet antiémétique de
l’ondansétron.
+ PAROXETINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ QUINIDINE
Association DECONSEILLEEDiminution de l’efficacité de l’opiacé par inhibition de son
métabolisme par l’inhibiteur.
+ TERBINAFINE
Association DECONSEILLEERisque d’inefficacité de l’opiacé par inhibition de son métabolisme
par l’inhibiteur.
+ VENLAFAXINE
A prendre en compteRisque d'apparition de convulsions et/ou d'un syndrome
sérotoninergique.
TRASTUZUMAB EMTANSINE
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEEAugmentation des concentrations plasmatiques du DM1, un
composant du trastuzumab emtansine, par inhibition de son
métabolisme par l’inhibiteur.
TRÉTINOÏNE
Voir aussi : rétinoïdes
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Adaptation de la posologie de la trétinoïne pendant le traitement par
l’inhibiteur et après son arrêt.
Décrit pour les antifongiques azolés
Augmentation des concentrations de trétinoïne par diminution de
son métabolisme, avec risque de majoration de sa toxicité (pseudo-
tumor cerebrii, hypercalcémie…)
TRICLABENDAZOLE
+ DIHYDROERGOTAMINE
CONTRE-INDICATION
Respecter un délai de 24 heures entre l’arrêt du triclabendazole et la
prise du médicament dérivé de l’ergot, et inversement.
Ergotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l’alcaloïde de l’ergot de seigle).
+ ERGOTAMINE
CONTRE-INDICATION
Respecter un délai de 24 heures entre l’arrêt du triclabendazole et
l’ergotamine, et inversement.
Ergotisme avec possibilité de nécrose des extrémités (inhibition du
métabolisme hépatique de l’alcaloïde de l’ergot de seigle).
+ PIMOZIDE
CONTRE-INDICATION
Respecter un délai de 24 heures entre l’arrêt du triclabendazole et la
prise du médicament torsadogène, et inversement.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes (inhibition du métabolisme hépatique du
médicament torsadogène).
+ QUINIDINE
Précaution d'emploi
Surveillance clinique.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes (inhibition du métabolisme hépatique du
médicament torsadogène).
TRIENTINE
+ FER
Précaution d'emploi
Prendre la trientine à distance des sels de fer.
Diminution des concentrations de fer sérique.
249
TRIMETHOPRIME
Voir aussi : hyperkaliémiants - sulfaméthoxazole + triméthoprime
+ CICLOSPORINE
A prendre en compteAvec le triméthoprime (seul ou associé) par voie orale :
augmentation de la créatininémie avec diminution possible des
concentrations sanguines de ciclosporine.
Avec le trimethoprime (seul ou associé) par voie IV : la diminution
des concentrations sanguines de ciclosporine peut être très
importante avec disparition possible du pouvoir
immunosuppresseur.
+ METHOTREXATE
CI - ASDEC
Contre-indication
- avec le méthotrexate utilisé à doses > 20 mg/semaine
Association déconseillée
- Avec le méthotrexate utilisé à des doses =< 20 mg/semaine
Augmentation de la toxicité hématologique du méthotrexate
(diminution de son excrétion rénale ainsi qu'inhibition de la
dihydrofolate réductase).
+ PACLITAXEL
Précaution d'emploi
Surveillance clinique et biologique étroite et adaptation de la posologie
du paclitaxel pendant l’association.
Risque d’augmentation des concentrations plasmatiques du
paclitaxel par inhibition de son métabolisme hépatique par le
triméthoprime.
+ PYRIMETHAMINE
Précaution d'emploi
Contrôle régulier de l'hémogramme et association d'un traitement par
l'acide folique (injections IM régulières).
Anémie mégaloblastique, plus particulièrement à fortes doses des
deux produits (déficit en acide folique par l'association de deux 2-4
diaminopyrimidines).
+ REPAGLINIDE
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite.
Risque d’augmentation des concentrations plasmatiques de
répaglinide par inhibition de son métabolisme hépatique par le
triméthoprime.
+ SELEXIPAG
Précaution d'emploi
Surveillance clinique étroite pendant l’association. Réduire de moitié la
posologie (une seule prise par jour).
Risque d’augmentation des effets indésirables du sélexipag par
diminution de son métabolisme.
TRIPTANS
(almotriptan, eletriptan, frovatriptan, naratriptan, rizatriptan, sumatriptan, zolmitriptan)
+ ALCALOÏDES DE L'ERGOT DE SEIGLE VASOCONSTRICTEURS
CONTRE-INDICATION
Respecter un délai de 6 à 24 heures, selon le triptan, entre la prise de
celui-ci et celle de l'alcaloïde ergoté
Risque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ INHIBITEURS SÉLECTIFS DE LA RECAPTURE DE LA SÉROTONINE
A prendre en compteRisque d'apparition d'un syndrome sérotoninergique.
TRIPTANS MÉTABOLISÉS PAR LA MAO
(almotriptan, rizatriptan, sumatriptan, zolmitriptan)
+ IMAO IRRÉVERSIBLES
CONTRE-INDICATIONRisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
CONTRE-INDICATIONRisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ IMAO-B
CONTRE-INDICATIONRisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
250
TRIPTANS NON MÉTABOLISÉS PAR LA MAO
(eletriptan, frovatriptan, naratriptan)
+ IMAO IRRÉVERSIBLES
Association DECONSEILLEERisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ IMAO-A RÉVERSIBLES, Y COMPRIS OXAZOLIDINONES ET BLEU DE MÉTHYLÈNE
Association DECONSEILLEERisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
+ IMAO-B
Association DECONSEILLEERisque d'hypertension artérielle, de vasoconstriction artérielle
coronaire.
TUCATINIB
Voir aussi : inhibiteurs de tyrosine kinases métabolisés - inhibiteurs puissants du CYP3A4
+ GEMFIBROZIL
Association DECONSEILLEEAugmentation importante des concentrations de tucatinib par
diminution de son métabolisme par le gemfibrozil.
ULIPRISTAL
Voir aussi : substances à absorption réduite par les topiques gastro-intestinaux, antiacides et adsorbants
+ ANTISÉCRÉTOIRES ANTIHISTAMINIQUES H2
A prendre en compteRisque de diminution de l’effet de l’ulipristal, par diminution de son
absorption.
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
A prendre en compteRisque de diminution de l’effet de l’ulipristal, par diminution de son
absorption.
+ CYPROTERONE
ASDEC - APEC
Association déconseillée
Dans l'utilisation à visée contraceptive de la cyprotérone
- Dans l'indication contraception d'urgence de l'ulipristal
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception additionnelle de type mécanique
pendant les 12 jours qui suivent la (dernière) prise de l’ulipristal (au cas
où il y en aurait eu plus d’une).
- Dans l’indication fibrome de l'ulipristal :
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception de type mécanique pendant les 7
premiers jours de la contraception hormonale.
Association à prendre en compte
Lorsque la cyprotérone n'est pas à visée contraceptive.
Dans l'indication contraception d'urgence de l'ulipristal :
Antagonisme des effets de l’ulipristal en cas de reprise d’un
contraceptif hormonal moins de 5 jours après la prise de la
contraception d’urgence.
Dans l’indication fibrome de l'ulipristal :
Antagonisme réciproque des effets de l’ulipristal et du progestatif,
avec risque d’inefficacité.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par l’inducteur.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par le ritonavir.
+ MILLEPERTUIS
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par l’inducteur.
251
+ PROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEE
- Dans l'indication contraception d'urgence:
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception additionnelle de type mécanique
pendant les 12 jours qui suivent la (dernière) prise de l’ulipristal (au cas
où il y en aurait eu plus d’une).
- Dans l’indication fibrome :
Dans le cas où la (re)prise d’une contraception hormonale est
envisagée, utiliser une contraception de type mécanique pendant les 7
premiers jours de la contraception hormonale.
Dans l'indication contraception d'urgence :
Antagonisme des effets de l’ulipristal en cas de reprise d’un
contraceptif hormonal moins de 5 jours après la prise de la
contraception d’urgence.
Dans l’indication fibrome :
Antagonisme réciproque des effets de l’ulipristal et du progestatif,
avec risque d’inefficacité.
+ PROGESTATIFS NON CONTRACEPTIFS, ASSOCIÉS OU NON À UN ESTROGÈNE
A prendre en compteDans l’indication fibrome :
Antagonisme réciproque des effets de l’ulipristal et du progestatif,
avec risque d’inefficacité.
+ RIFAMPICINE
Association DECONSEILLEE
Préférer une alternative thérapeutique peu ou pas métabolisée.
Risque de diminution de l’effet de l’ulipristal, par augmentation de
son métabolisme hépatique par l’inducteur.
VACCINS VIVANTS ATTÉNUÉS
(bcg, rotavirus, virus de la fievre jaune, virus de la rougeole, virus des oreillons, virus rubeoleux, virus varicelle-zona, virus vivant atténué de la grippe)
+ ABATACEPT
Association DECONSEILLEE
ainsi que pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée, éventuellement mortelle.
+ ANTICORPS MONOCLONAUX (HORS ANTI-TNF ALPHA)
ASDEC - APEC
Association déconseillée avec :
- anifrolumab, atézolizumab, bélimumab, bimékizumab, blinatumomab,
canakinumab, durvalumab, guselkumab, inébilizumab, inotuzumab,
ixékizumab, obinutuzumab, ocrélizumab, ofatumumab, rituximab,
sacituzumab, spésolimab, tafasitamab, tézépelumab, tocilizumab,
ustékinumab
A prendre en compte avec :
- alemtuzumab, amivantamab, brentuximab, cetuximab, daratumumab,
dénosumab, ibritumomab, ipilimumab, natalizumab, nivolumab,
panitumumab, pembrolizumab, ramucirumab, satralizumab,
sécukinumab, siltuximab, tralokinumab, védolizumab
Risque de maladie vaccinale généralisée, éventuellement mortelle.
+ ANTI-TNF ALPHA
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
+ BÉLATACEPT
Association DECONSEILLEERisque de maladie vaccinale généralisée, éventuellement mortelle.
+ CYTOTOXIQUES
CONTRE-INDICATION
- Et pendant les 6 mois suivant l'arrêt de la chimiothérapie.
- Et, à l'exception de l'hydroxycarbamide dans son indication chez le
patient drépanocytaire.
Risque de maladie vaccinale généralisée éventuellement mortelle.
+ DIMÉTHYLE ( FUMARATE DE)
A prendre en comptePossible augmentation du risque infectieux.
+ GLOBULINES ANTILYMPHOCYTAIRES
A prendre en compte
En particulier, utiliser un vaccin inactivé lorsqu'il existe (poliomyélite).
Risque de maladie généralisée éventuellement mortelle. Ce risque
est majoré chez les sujets âgés déjà immunodéprimés par la
maladie sous-jacente.
+ GLUCOCORTICOÏDES (SAUF HYDROCORTISONE)
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt de la corticothérapie.
A l'exception des voies inhalées et locales, et pour des posologies
supérieures à 10 mg/j d’équivalent-prednisone (ou > 2 mg/kg/j chez
l’enfant ou > 20 mg/j chez l’enfant de plus de 10 kg) pendant plus
de deux semaines et pour les « bolus » de corticoïdes: risque de
maladie vaccinale généralisée éventuellement mortelle.
252
+ HYDROXYCARBAMIDE
Association DECONSEILLEE
L'association ne devra être envisagée que si les bénéfices sont estimés
comme étant supérieurs à ce risque.
S'il est décidé d’interrompre le traitement par hydroxycarbamide pour
effectuer la vaccination, un délai de 3 mois après l’arrêt est
recommandé.
Dans son indication chez le patient drépanocytaire, risque
théorique de maladie vaccinale généralisée.
+ IMMUNOSUPPRESSEURS
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
+ MYCOPHENOLATE MOFETIL
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
+ MYCOPHENOLATE SODIQUE
CONTRE-INDICATION
Et pendant les 3 mois suivant l'arrêt du traitement.
Risque de maladie vaccinale généralisée éventuellement mortelle.
+ TÉRIFLUNOMIDE
Association DECONSEILLEERisque de maladie vaccinale généralisée, éventuellement mortelle.
VALGANCICLOVIR
Voir aussi : médicaments néphrotoxiques
+ FLUCYTOSINE
A prendre en compteRisque de majoration de la toxicité hématologique.
+ MARIBAVIR
CONTRE-INDICATIONAntagonisme de la phosporylation et donc de l'effet
pharmacologique du valganciclovir par le maribavir.
VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
(acide valproique, valpromide)
+ ACETAZOLAMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
+ AZTREONAM
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation éventuelle de
la posologie de l'anticonvulsivant pendant le traitement par l'anti-
infectieux et après son arrêt.
Risque de survenue de crises convulsives, par diminution des
concentrations plasmatiques de l'acide valproïque.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique, dosages plasmatiques et adaptation de la
posologie des deux anticonvulsivants.
Augmentation des concentrations plasmatiques du métabolite actif
de la carbamazépine avec signes de surdosage. De plus,
diminution des concentrations plasmatiques d'acide valproïque par
augmentation de son métabolisme hépatique par la carbamazépine.
+ FELBAMATE
Précaution d'emploi
Surveillance clinique, contrôle biologique et adaptation éventuelle de la
posologie du valproate ou du valpromide pendant le traitement par le
felbamate et après son arrêt.
Augmentation des concentrations plasmatiques de l'acide
valproïque, avec risque de surdosage.
+ LAMOTRIGINE
Association DECONSEILLEE
Si l'association s'avère nécessaire, surveillance clinique étroite.
Risque majoré de réactions cutanées graves (syndrome de Lyell).
Par ailleurs, augmentation des concentrations plasmatiques de
lamotrigine (diminution de son métabolisme hépatique par le
valproate de sodium).
+ NIMODIPINE
A prendre en compteAvec la nimodipine par voie orale, et par extrapolation, par voie
injectable : risque de majoration de l'effet hypotenseur de la
nimodipine par augmentation de ses concentrations plasmatiques
(diminution de son métabolisme par l'acide valproïque).
253
+ PÉNEMS
Association DECONSEILLEERisque de survenue de crises convulsives, par diminution rapide
des concentrations plasmatiques de l’acide valproïque, pouvant
devenir indétectables.
+ PHÉNOBARBITAL (ET, PAR EXTRAPOLATION, PRIMIDONE)
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
+ PHÉNYTOÏNE (ET, PAR EXTRAPOLATION, FOSPHÉNYTOÏNE)
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique et biologique, et adaptation éventuelle de la
posologie de l'anticonvulsivant pendant le traitement par la rifampicine
et après son arrêt.
Risque de survenue de crises convulsives, par augmentation du
métabolisme hépatique du valproate par la rifampicine.
+ RUFINAMIDE
Précaution d'emploi
Chez l’enfant de moins de 30 kg :
ne pas dépasser la dose totale de 600 mg/j après la période de titration.
Possible augmentation des concentrations de rufinamide,
notamment chez l’enfant de moins de 30 kg.
+ TOPIRAMATE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
+ ZIDOVUDINE
Précaution d'emploi
Surveillance clinique et biologique régulière. Un hémogramme à la
recherche d’une anémie devrait être réalisé au cours des deux premiers
mois de l’association.
Risque d’augmentation des effets indésirables, notamment
hématologiques, de la zidovudine par diminution de son
métabolisme par l’acide valproïque.
+ ZONISAMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
VANCOMYCINE
Voir aussi : médicaments néphrotoxiques - médicaments ototoxiques
+ PIPÉRACILLINE/TAZOBACTAM
Association DECONSEILLEEMajoration de la néphrotoxicité par comparaison à la vancomycine
seule.
VARDENAFIL
Voir aussi : inhibiteurs de la phosphodiesterase de type 5 - médicaments à l'origine d'une hypotension orthostatique
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations plasmatiques du vardénafil, avec
risque d’hypotension.
VELPATASVIR
+ ANTISÉCRÉTOIRES INHIBITEURS DE LA POMPE À PROTONS
Association DECONSEILLEE
Si l’association s’avère nécessaire, la bithérapie velpatasvir/sofosbuvir
doit être prise au moment du repas, ou 4 heures avant la prise d’un IPP
donné à dose minimale.
Diminution des concentrations de velpatasvir et de sofosbuvir.
+ EFAVIRENZ
Association DECONSEILLEERisque de diminution des concentrations de velpatasvir/sofosbuvir,
avec possible retentissement sur l’efficacité.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par
l’inducteur, avec possible retentissement sur l’efficacité.
254
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par le
millepertuis, avec possible retentissement sur l’efficacité.
+ OXCARBAZEPINE
Association DECONSEILLEERisque de diminution des concentrations de velpatasvir/sofosbuvir,
avec possible retentissement sur l’efficacité.
+ RIFABUTINE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par la
rifabutine, avec possible retentissement sur l’efficacité.
+ RIFAMPICINE
CONTRE-INDICATIONDiminution des concentrations plasmatiques de velpatasvir par la
rifampicine, avec possible retentissement sur l’efficacité.
+ ROSUVASTATINE
Précaution d'emploi
En cas d’association, ne pas dépasser 10 mg par jour de rosuvastatine.
Augmentation des concentrations plasmatiques de rosuvastatine
par augmentation de son absorption intestinale par le velpatasvir.
VÉMURAFÉNIB
+ BUPROPION
A prendre en compteRisque de diminution des concentrations du bupropion, avec
augmentation de son métabolite actif et toxicité majorée.
+ ESTROPROGESTATIFS CONTRACEPTIFS
Association DECONSEILLEERisque de diminution des concentrations des estroprogestatifs,
avec pour conséquence un risque d’inefficacité.
+ IFOSFAMIDE
A prendre en compteRisque de diminution des concentrations de l'ifosfamide, avec
augmentation de son métabolite actif et toxicité majorée.
+ IMMUNOSUPPRESSEURS
Association DECONSEILLEERisque de diminution des concentrations des
immunosuppresseurs, avec pour conséquence un risque
d’inefficacité.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEERisque de diminution des concentrations du vémurafénib, avec
moindre efficacité.
+ THEOPHYLLINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la théophylline
pendant le traitement par vémurafénib et après son arrêt.
Augmentation importante des concentrations de théophylline, avec
risques de majoration de ses effets indésirables.
VÉNÉTOCLAX
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment hématologique,
et adaptation de la posologie du vénétoclax.
Risque d’augmentation des effets indésirables du vénétoclax par
diminution de son métabolisme hépatique.
+ DILTIAZEM
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment hématologique,
et adaptation de la posologie du vénétoclax.
Risque d’augmentation des effets indésirables du vénétoclax par
diminution de son métabolisme hépatique.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution importante des concentrations de vénétoclax, avec
risque de perte d’efficacité.
255
+ INHIBITEURS PUISSANTS DU CYP3A4
CI - PE
Contre-indication :
- pendant la phase de titration.
Précaution d'emploi:
- réduction de posologie de 75% en phase de stabilisation.
Augmentation très importante des concentrations de vénétoclax par
diminution de son métabolisme hépatique, avec risque de
majoration de la toxicité, notamment hématologique.
+ MILLEPERTUIS
CONTRE-INDICATIONDiminution importante des concentrations de vénétoclax, avec
risque de perte d’efficacité.
+ PAMPLEMOUSSE (JUS ET FRUIT)
Association DECONSEILLEEAugmentation des concentrations de vénétoclax, avec risque de
majoration des effets indésirables.
+ VERAPAMIL
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment hématologique,
et adaptation de la posologie du vénétoclax.
Risque d’augmentation des effets indésirables du vénétoclax par
diminution de son métabolisme hépatique.
VENLAFAXINE
Voir aussi : médicaments mixtes adrénergiques-sérotoninergiques - médicaments à l'origine d'un syndrome sérotoninergique
+ CLARITHROMYCINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ ERYTHROMYCINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ ITRACONAZOLE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ KETOCONAZOLE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ TELITHROMYCINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
+ TRAMADOL
A prendre en compteRisque d'apparition de convulsions et/ou d'un syndrome
sérotoninergique.
+ VORICONAZOLE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
VERAPAMIL
Voir aussi : antagonistes des canaux calciques - antiarythmiques - antihypertenseurs sauf alpha-bloquants - bradycardisants - médicaments abaissant la pression
artérielle
+ AFATINIB
Précaution d'emploi
Il est recommandé d’administrer le vérapamil le plus à distance possible
de l’afatinib, en respectant de préférence un intervalle
de 6 heures ou de 12 heures par rapport à la prise d’afatinib.
Augmentation des concentrations plasmatique d’afatinib par
augmentation de son absorption par le vérapamil.
256
+ AMIODARONE
ASDEC - PE
Association déconseillée avec :
- le vérapamil IV
Si l'association ne peut être évitée, surveillance clinique et ECG continu.
Précaution d'emploi avec :
- le vérapamil per os
Surveillance clinique et ECG.
Pour vérapamil voie injectable :
-risque de bradycardie ou de bloc auriculo-ventriculaire.
Pour vérapamil per os :
-risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez les personnes âgées.
+ ANTIHYPERTENSEURS CENTRAUX
A prendre en compteTroubles de l'automatisme (troubles de la conduction auriculo-
ventriculaire par addition des effets négatifs sur la conduction).
+ ATORVASTATINE
Précaution d'emploi
Utiliser des doses plus faibles d'hypocholestérolémiant. Si l'objectif
thérapeutique n'est pas atteint, utiliser une autre statine non concernée
par ce type d'interaction.
Risque majoré d'effets indésirables (concentration-dépendants) à
type de rhabdomyolyse, par diminution du métabolisme hépatique
de l'hypocholestérolémiant.
+ BÊTA-BLOQUANTS (SAUF ESMOLOL) (Y COMPRIS COLLYRES)
Association DECONSEILLEE
Une telle association ne doit se faire que sous surveillance clinique et
ECG étroite, en particulier chez le sujet âgé ou en début de traitement.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
trouble de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
+ BÊTA-BLOQUANTS DANS L'INSUFFISANCE CARDIAQUE
Association DECONSEILLEEEffet inotrope négatif avec risque de décompensation de
l’insuffisance cardiaque, troubles de l'automatisme (bradycardie,
arrêt sinusal) et troubles de la conduction sino-auriculaire et
auriculo-ventriculaire.
+ BUSPIRONE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la buspirone si
nécessaire.
Augmentation des concentrations plasmatiques de la buspirone par
diminution de son métabolisme hépatique par le vérapamil, avec
augmentation de ses effets indésirables.
+ CARBAMAZEPINE
Précaution d'emploi
Surveillance clinique et adaptation éventuelle des posologies des deux
médicaments.
Augmentation des concentrations de carbamazépine et de sa
neurotoxicité par inhibition de son métabolisme par le vérapamil.
De plus, diminution des concentrations du vérapamil par
augmentation de son métabolisme par la carbamazépine.
+ CICLOSPORINE
Précaution d'emploi
Dosage des concentrations sanguines de la ciclosporine, contrôle de la
fonction rénale et adaptation de la posologie pendant l’association et
après son arrêt.
Augmentation des concentrations sanguines de la ciclosporine
(diminution de son métabolisme hépatique), et majoration du risque
de gingivopathies.
+ COLCHICINE
Association DECONSEILLEERisque de majoration des effets indésirables de la colchicine, par
augmentation de ses concentrations plasmatiques par le vérapamil.
+ DABIGATRAN
Précaution d'emploi
Dans l'indication post-chirurgicale : surveillance clinique et adaptation
de la posologie du dabigatran à 150 mg/j en une prise, voire 75 mg/j en
cas d'insuffisance rénale modérée.
Dans l'indication fibrillation auriculaire : surveillance clinique et
adaptation de la posologie du dabigatran à 220 mg/j en deux prises.
Augmentation des concentrations plasmatiques de dabigatran,
avec majoration du risque de saignement.
+ DANTROLENE
CONTRE-INDICATIONAvec le dantrolène administré par perfusion : chez l'animal, des cas
de fibrillations ventriculaires mortelles sont constamment observés
lors de l'administration de vérapamil et de dantrolène par voie IV.
L'association d'un antagoniste du calcium et de dantrolène est donc
potentiellement dangereuse. Cependant, quelques patients ont
reçu l'association nifédipine et dantrolène sans inconvénient.
+ DIGOXINE
Précaution d'emploi
Surveillance clinique, ECG et, éventuellement, contrôle de la
digoxinémie. S'il y a lieu, adaptation de la posologie de la digoxine
pendant le traitement par le vérapamil et après son arrêt.
Bradycardie excessive et bloc auriculo-ventriculaire par majoration
des effets de la digoxine sur l'automatisme et la conduction et par
diminution de l'élimination rénale et extrarénale de la digoxine.
+ DOXORUBICINE
A prendre en compteRisque de majoration de la toxicité de la doxorubicine par
augmentation de ses concentrations plasmatiques.
257
+ DRONEDARONE
Précaution d'emploi
Débuter le traitement par l’antagoniste calcique aux posologies
minimales recommandées, et ajuster les doses en fonction de l’ECG.
Risque de bradycardie ou de bloc auriculo-ventriculaire, notamment
chez le sujet âgé. Par ailleurs, légère augmentation des
concentrations de dronédarone par diminution de son métabolisme
par l’antagoniste des canaux calciques.
+ ERYTHROMYCINE
Précaution d'emploi
Surveillance clinique et ECG ; s'il y a lieu, adaptation de la posologie du
vérapamil pendant le traitement par l'érythromycine et après son arrêt.
Bradycardie et/ou troubles de la conduction auriculo-ventriculaire,
par diminution du métabolisme hépatique du vérapamil par
l'érythromycine.
+ ESMOLOL
ASDEC - PE
Association déconseillée :
- en cas d'altération de la fonction ventriculaire gauche.
Précaution d'emploi :
- si la fonction ventriculaire gauche est normale.
Surveillance clinique et ECG.
Troubles de l'automatisme (bradycardie excessive, arrêt sinusal),
troubles de la conduction sino-auriculaire et auriculo-ventriculaire et
défaillance cardiaque.
+ EVEROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines de l'évérolimus par
diminution de son métabolisme hépatique par le vérapamil.
+ FIDAXOMICINE
Association DECONSEILLEEAugmentation des concentrations plasmatiques de la fidaxomicine.
+ IBRUTINIB
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique étroite et
réduction de la dose d’ibrutinib à 280 mg par jour pendant la durée de
l’association.
Risque d’augmentation des concentrations plasmatiques d’ibrutinib
par diminution de son métabolisme hépatique par le vérapamil.
+ INHIBITEURS PUISSANTS DU CYP3A4
Précaution d'emploi
Surveillance clinique et ECG. S’il y a lieu, adaptation de la posologie du
vérapamil pendant le traitement par l’inhibiteur, et après son arrêt, le
cas échéant.
Bradycardie et/ou troubles de la conduction auriculo-ventriculaire,
par diminution du métabolisme hépatique du vérapamil par
l’inhibiteur.
+ IVABRADINE
CONTRE-INDICATIONAugmentation des concentrations plasmatiques de l’ivabradine et
de ses effets indésirables, notamment cardiaques (augmentation
de son absorption et inhibition de son métabolisme hépatique par le
vérapamil), qui s’ajoutent aux effets bradycardisants de ces deux
médicaments.
+ MIDAZOLAM
Précaution d'emploi
Surveillance clinique et réduction de la posologie de midazolam
pendant le traitement par le vérapamil.
Augmentation des concentrations plasmatiques de midazolam
(diminution de son métabolisme hépatique avec majoration de la
sédation).
+ MILLEPERTUIS
CONTRE-INDICATIONRéduction importante des concentrations de vérapamil, avec risque
de perte de son effet thérapeutique.
+ NALOXEGOL
Précaution d'emploi
Adaptation posologique pendant l’association.
Augmentation des concentrations plasmatiques de naloxegol par le
vérapamil.
+ NINTÉDANIB
Précaution d'emploi
Surveillance clinique pendant l’association.
Augmentation des concentrations plasmatiques du nintédanib par
augmentation de son absorption par le vérapamil.
+ OLAPARIB
Association DECONSEILLEE
Si l’association ne peut être évitée, limiter la dose d’olaparib à 200 mg
deux fois par jour.
Augmentation des concentrations plasmatiques d’olaparib par le
vérapamil.
+ PAMPLEMOUSSE (JUS ET FRUIT)
A prendre en compteAugmentation des concentrations plasmatiques de vérapamil, avec
risque de survenue d’effets indésirables.
258
+ PIMOZIDE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaires, notamment, de
torsades de pointes.
+ QUINIDINE
Association DECONSEILLEERisque de majoration importante des effets hémodynamiques du
vérapamil, avec hypotension et bradycardie sévères.
+ SIMVASTATINE
Précaution d'emploi
Ne pas dépasser la posologie de 20 mg/j de simvastatine ou utiliser une
autre statine non concernée par ce type d’interaction.
Risque majoré d’effets indésirables (dose-dépendants) à type de
rhabdomyolyse (diminution du métabolisme hépatique de
l’hypocholestérolémiant).
+ SIROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines du sirolimus
(diminution de son métabolisme hépatique par le vérapamil).
+ TACROLIMUS
Précaution d'emploi
Dosage des concentrations sanguines de l’immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l’association et après son arrêt.
Augmentation des concentrations sanguines du tacrolimus
(diminution de son métabolisme hépatique par le verapamil).
+ TALAZOPARIB
Précaution d'emploi
Réduire la dose de talazoparib.
Augmentation des concentrations de talazoparib avec risque de
majoration de la toxicité.
+ TAMSULOSINE
Précaution d'emploi
Surveillance clinique et adaptation de la posologie de la tamsulosine
pensant le traitement par l’inhibiteur enzymatique et après son arrêt, le
cas échéant.
Risque de majoration des effets indésirables de la tamsulosine, par
inhibition de son métabolisme hépatique.
+ TÉNOFOVIR ALAFÉNAMIDE
Précaution d'emploi
En cas de co-administration avec le vérapamil, la dose de ténofovir
alafénamide doit être limitée à 10 mg par jour.
Augmentation des concentrations plasmatiques du ténofovir
alafénamide par augmentation de son absorption.
+ TICAGRELOR
A prendre en compteRisque d’augmentation des concentrations plasmatiques de
ticagrelor par diminution de son métabolisme hépatique.
+ TOLVAPTAN
Précaution d'emploi
Réduire la posologie de tolvaptan de moitié.
Augmentation des concentrations de tolvaptan, avec risque de
majoration importante des effets indésirables, notamment diurèse
importante, déshydratation, insuffisance rénale aiguë.
+ VÉNÉTOCLAX
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment hématologique,
et adaptation de la posologie du vénétoclax.
Risque d’augmentation des effets indésirables du vénétoclax par
diminution de son métabolisme hépatique.
VIDARABINE
+ ALLOPURINOL
Association DECONSEILLEERisque accru de troubles neurologiques (tremblements, confusion)
par inhibition partielle du métabolisme de l'antiviral.
VINCA-ALCALOÏDES CYTOTOXIQUES
(vinblastine, vincristine, vindesine, vinflunine, vinorelbine)
+ FLUCONAZOLE
Précaution d'emploi
Surveillance clinique et biologique étroite pendant l’association.
Risque de majoration de la toxicité de l’antimitotique par diminution
de son métabolisme hépatique par le fluconazole.
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEEDiminution des concentrations plasmatiques du vinca-alcaloïde par
l’inducteur, avec possible retentissement sur l’efficacité..
259
+ INHIBITEURS PUISSANTS DU CYP3A4
Association DECONSEILLEE
Si l’association ne peut être évitée, surveillance clinique et biologique
étroite.
Risque de majoration de la toxicité de l'antimitotique par diminution
de son métabolisme hépatique par l’inhibiteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de moindre efficacité du cytotoxique par augmentation de
son métabolisme par le millepertuis.
+ MITOMYCINE C
A prendre en compteRisque de majoration de la toxicité pulmonaire de la mitomycine et
des vinca-alcaloïdes.
VISMODÉGIB
+ INDUCTEURS ENZYMATIQUES
Association DECONSEILLEERisque de diminution des concentrations plasmatiques de
vismodegib par augmentation de son métabolisme hépatique par
l’inducteur.
+ MILLEPERTUIS
CONTRE-INDICATIONRisque de diminution des concentrations plasmatiques de
vismodégib.
VITAMINE A
+ CYCLINES
CONTRE-INDICATIONEn cas d'apport de 10,000 UI/j et plus : risque d’hypertension
intracrânienne.
+ RÉTINOÏDES
CONTRE-INDICATIONRisque de symptômes évocateurs d’une hypervitaminose A.
VITAMINE D
(alfacalcidol, calcitriol, cholecalciferol, ergocalciferol)
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Précaution d'emploi
Dosage des concentrations de vitamine D et supplémentation si
nécessaire.
Diminution des concentrations de vitamine D plus marquée qu’en
l’absence d'inducteur.
+ ORLISTAT
A prendre en compteDiminution de l'absorption de la vitamine D.
+ RIFAMPICINE
Précaution d'emploi
Dosage des concentrations de vitamine D et supplémentation si
nécessaire.
Diminution des concentrations de vitamine D plus marquée qu’en
l’absence de traitement par la rifampicine
VORICONAZOLE
Voir aussi : inhibiteurs puissants du CYP3A4
+ AMIODARONE
Précaution d'emploi
Surveillance clinique et ECG, et adaptation éventuelle de la posologie
de l’amiodarone.
Risque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes, par possible diminution du métabolisme de
l’amiodarone.
+ ANTIVITAMINES K
Précaution d'emploi
Contrôle plus fréquent de l'INR. Adaptation éventuelle de la posologie
de l'antivitamine K pendant le traitement par voriconazole et 8 jours
après son arrêt.
Augmentation de l'effet de l'antivitamine K et du risque
hémorragique par diminution de son métabolisme hépatique.
+ EFAVIRENZ
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite et
adaptation de la posologie du voriconazole et de l'éfavirenz pendant
l'association.
Risque de baisse de l'efficacité du voriconazole par augmentation
de son métabolisme hépatique par l'efavirenz.
260
+ FLUCLOXACILLINE
Association DECONSEILLEEDiminution des concentrations de voriconazole, avec risque
d'inefficacité de l'antifongique azolé.
+ GLIPIZIDE
Précaution d'emploi
Prévenir le patient, renforcer l'autosurveillance glycémique et adapter
éventuellement la posologie du sulfamide pendant et après le traitement
par voriconazole.
Risque d’augmentation des concentrations plasmatiques du
glipizide à l’origine d’hypoglycémies potentiellement sévères.
+ IMMUNOSUPPRESSEURS
ASDEC - PE
Association déconseillée
- avec l'évérolimus, le sirolimus, et le temsirolimus.
Précaution d'emploi
- avec la ciclosporine et le tacrolimus :
dosage des concentrations sanguines de l'immunosuppresseur,
contrôle de la fonction rénale et adaptation de la posologie pendant
l'association et après son arrêt.
Augmentation des concentrations sanguines de
l'immunosuppresseur par inhibition de son métabolisme hépatique
par le voriconazole.
+ INDUCTEURS ENZYMATIQUES PUISSANTS
CI - ASDEC
Contre-indication :
- pour carbamazépine, phénobarbital, primidone
Association déconseillée :
- pour apalutamide, enzalutamide
- pour phénytoïne, fosphénytoïne
Si l'association ne peut être évitée, surveillance clinique étroite, dosage
des concentrations plasmatiques de phénytoïne et adaptation
éventuelle des posologies pendant l'association et après l'arrêt du
voriconazole.
- pour carbamazépine, phénobarbital, primidone : Risque de baisse
de l'efficacité du voriconazole par augmentation de son
métabolisme hépatique par l'inducteur.
- pour phénytoïne, fosphénytoïne :
Diminution importante des concentrations plasmatiques du
voriconazole avec risque de perte d'efficacité, par augmentation de
son métabolisme hépatique par la phénytoïne, d'une part, et
augmentation des concentrations plasmatiques de la phénytoïne
par diminution de son métabolisme hépatique par le voriconazole,
d'autre part.
+ INHIBITEURS DE PROTÉASES BOOSTÉS PAR RITONAVIR
Association DECONSEILLEEBaisse très importante des concentrations de l’antifongique par
augmentation de son métabolisme par le ritonavir, avec risque
d’échec du traitement.
+ LÉTERMOVIR
Association DECONSEILLEE
Si l’association s’avère nécessaire, surveillance clinique étroite,
notamment les deux premières semaines après l’instauration ou l’arrêt
du traitement par létermovir.
Diminution de plus de la moitié de l’exposition du voriconazole.
+ METHADONE
Précaution d'emploi
Surveillance clinique et électrocardiographique renforcée ; si besoin,
adaptation de la posologie de la méthadone pendant le traitement par le
voriconazole et après son arrêt.
Augmentation des concentrations plasmatiques de méthadone
avec surdosage et risque majoré d’allongement de l’intervalle QT et
de troubles du rythme ventriculaire, notamment de torsades de
pointes.
+ MILLEPERTUIS
CONTRE-INDICATIONRéduction importante des concentrations de voriconazole, avec
risque de perte de son effet thérapeutique.
+ NEVIRAPINE
Association DECONSEILLEE
Si l'association ne peut être évitée, surveillance clinique étroite et
adaptation éventuelle de la posologie du voriconazole pendant
l'association.
Risque de baisse de l'efficacité du voriconazole par augmentation
de son métabolisme hépatique par la névirapine.
+ QUINIDINE
CONTRE-INDICATIONRisque majoré de troubles du rythme ventriculaire, notamment de
torsades de pointes.
+ RIFABUTINE
Association DECONSEILLEE
Si l'association est jugée néccessaire, surveillance clinique et
adaptation de la posologie du voriconazole (en général doublée)
pendant le traitement par la rifabutine.
Diminution des concentrations plasmatiques du voriconazole avec
risque de perte d'efficacité, par augmentation de son métabolisme
hépatique par la rifabutine d'une part, et risque d'augmentation des
effets indésirables (uvéites) de la rifabutine d'autre part.
+ RIFAMPICINE
CONTRE-INDICATIONDiminution importante des concentrations plasmatiques du
voriconazole avec risque de perte d'efficacité, par augmentation de
son métabolisme hépatique par la rifampicine.
261
+ VENLAFAXINE
A prendre en compteAugmentation des concentrations de venlafaxine avec risque de
surdosage.
VOXELOTOR
+ INDUCTEURS ENZYMATIQUES PUISSANTS
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du voxelotor,
avec risque de moindre efficacité.
+ RIFAMPICINE
Association DECONSEILLEEDiminution notable des concentrations plasmatiques du voxelotor,
avec risque de moindre efficacité.
YOHIMBINE
+ ANTIHYPERTENSEURS CENTRAUX
Association DECONSEILLEEInhibition possible de l'activité antihypertensive par antagonisme au
niveau des récepteurs.
ZIDOVUDINE
+ AMPHOTERICINE B
Précaution d'emploi
Contrôle plus fréquent de l'hémogramme.
Avec l'amphotéricine B administrée par voie IV : augmentation de
la toxicité hématologique (addition d'effets de toxicité médullaire).
+ DAPSONE
Précaution d'emploi
Contrôle plus fréquent de l'hémogramme.
Augmentation de la toxicité hématologique (addition d'effets de
toxicité médullaire).
+ FLUCYTOSINE
Précaution d'emploi
Contrôle plus fréquent de l'hémogramme.
Augmentation de la toxicité hématologique (addition d'effets de
toxicité médullaire).
+ GANCICLOVIR
Précaution d'emploi
Arrêter de façon transitoire la zidovudine ; contrôler la NFS et
réintroduire, si possible, la zidovudine à doses faibles.
Augmentation de la toxicité hématologique (addition d'effets de
toxicité médullaire).
+ RIBAVIRINE
Précaution d'emploi
Surveillance clinique et biologique régulière, notamment en début
d'association.
Risque de diminution de l'efficacité de chaque antiviral, par
antagonisme compétitif de la réaction de phosphorylation à l'origine
des métabolites actifs.
+ RIFAMPICINE
Association DECONSEILLEE
Si l'association s'avère nécessaire, surveillance clinique et biologique
renforcée.
Diminution de moitié des concentrations de la zidovudine par
augmentation de son métabolisme par la rifampicine.
+ STAVUDINE
Association DECONSEILLEERisque de diminution de l'efficacité de chaque antiviral par
antagoniste compétitif de la réaction de phosphorylation à l'origine
des métabolites actifs.
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière. Un hémogramme à la
recherche d’une anémie devrait être réalisé au cours des deux premiers
mois de l’association.
Risque d’augmentation des effets indésirables, notamment
hématologiques, de la zidovudine par diminution de son
métabolisme par l’acide valproïque.
ZINC
+ CALCIUM
Précaution d'emploi
Prendre les sels de calcium à distance du zinc (plus de 2 heures si
possible).
Diminution de l’absorption digestive du zinc par le calcium.
262
+ CYCLINES
Précaution d'emploi
Prendre les sels de zinc à distance des cyclines (plus de 2 heures si
possible).
Diminution de l'absorption digestive des cyclines.
+ FER
Précaution d'emploi
Prendre les sels de fer à distance du zinc (plus de 2 heures si possible).
Diminution de l’absorption digestive du zinc par le fer.
+ FLUOROQUINOLONES
Précaution d'emploi
Prendre les sels de zinc à distance des fluoroquinolones (plus de 2
heures, si possible).
Diminution de l'absorption digestive des fluoroquinolones.
+ INHIBITEURS D'INTÉGRASE
Précaution d'emploi
Prendre les sels de zinc à distance de l’antirétroviral (plus de 2 heures,
si possible).
Risque de diminution de l'absorption digestive des inhibiteurs
d’intégrase, par chélation par le cation divalent.
+ STRONTIUM
Précaution d'emploi
Prendre le strontium à distance des sels de zinc (plus de deux heures,
si possible).
Diminution de l'absorption digestive du strontium.
ZOLPIDEM
Voir aussi : benzodiazépines et apparentés - hypnotiques - médicaments sédatifs
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en compteLégère augmentation de l'effet sédatif du zolpidem.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique. Utiliser éventuellement un autre hypnotique.
Diminution des concentrations plasmatiques et de l'efficacité du
zolpidem par augmentation de son métabolisme hépatique par la
rifampicine.
ZONISAMIDE
Voir aussi : anticonvulsivants métabolisés
+ VALPROÏQUE (ACIDE) ET, PAR EXTRAPOLATION, VALPROMIDE
Précaution d'emploi
Surveillance clinique et biologique régulière.
Augmentation de l'hyperammoniémie, avec risque accru
d'encéphalopathie.
ZOPICLONE
Voir aussi : benzodiazépines et apparentés - hypnotiques - médicaments sédatifs
+ INHIBITEURS PUISSANTS DU CYP3A4
A prendre en compteLégère augmentation de l'effet sédatif de la zopiclone.
+ RIFAMPICINE
Précaution d'emploi
Surveillance clinique. Utiliser éventuellement un autre hypnotique.
Diminution des concentrations plasmatiques et de l'efficacité de la
zopiclone par augmentation de son métabolisme hépatique par la
rifampicine.
"""

# Parse the interactions from the text
interactions = parse_interactions(text)

# Define the path where the JSON file will be saved
file_path = 'out/interaction.json'

# Save the interactions to a JSON file
save_interactions_to_json(interactions, file_path)

