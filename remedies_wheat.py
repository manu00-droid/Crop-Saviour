def remedy(disease):
    disease = disease.casefold()

    if disease == 'LEAF RUST'.casefold() or disease == 'STEM RUST'.casefold() or disease == 'YELLOW RUST'.casefold():
        remedy_text = """Most effective method for control of rust, is to grow rust-resistant varieties. 
Biodiversity among wheat cultivars can also effectively check the rust problem. 
Use 3-4 wheat varieties at a time on each farm. Avoid late sowing or late 
maturing varieties. To protect the crop from rust infection, spray 5 liters of 
sour buttermilk mixed with 200 liter of water. Amaranth (chaulai or lal bhaji – 
a common green leaf vegetable) or Mentha (Pudina) leaf dust can also be used as 
fine spray (25- 30 gm dry leaf powder per lit of water) to prevent the infection 
of rusts. Foliar spray of dry leaf extract of Hibiscus rosa-sinensis (China 
rose) can also prevent the rust infection."""

    elif disease == 'POWDERY MILDEW'.casefold():
        remedy_text = """1. Grow varieties resistant to the diseases.
2. Bum crop refuse in the field after the harvest is over.
3. If loss is expected to be high, spraying with a mixture of Dithane M-45 and 
Karathane has been found beneficial. Prepare mixture by mixing 16 parts of 
Dithane M-45 and 4 parts of Karathane-25 wettable powder. Spray mixture @ 2 
kg/ha dissolved in 1000 litres of water. About three sprays will be sufficient 
at an interval of 10-15 days. Amount of water for different sprays may be 
decided on the basis of growing stage of the crop."""

    elif disease == 'SEEDLINGS'.casefold():
        remedy_text = """NO REMEDY AVAILABLE"""

    elif disease == 'SEPTORIA'.casefold():
        remedy_text = """NO REMEDY AVAILABLE"""

    else:
        remedy_text = """CROP IS HEALTHY"""
