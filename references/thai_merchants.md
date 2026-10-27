# Thai Credit Card Merchant & Statement Reference Guide

This reference documents common Thai credit card transaction naming patterns, merchant abbreviations, and statement format differences.

---

## 1. Bank Statement Differences

### ttb (TMBThanachart Bank)
- **Table Columns:** `Transaction date | Posted date | Description | Amount`
- **Reversals & Payments:** Displayed with standard minus sign (e.g., `-15.00 THB`, `-4,242.00 THB`).
- **Installments:** Denoted with fraction format (e.g., `001/010`, `002/003`).
- **Commute EMV Rebates:** Often appear as `-15.00 THB` (`BTS LAT PHRAO BANGKOK TH`) due to joint transit transfer discounts.

### UOB (United Overseas Bank)
- **Table Columns:** `POST DATE | TRANS DATE | DESCRIPTION | AMOUNT (THB)`
- **Reversals & Payments:** Denoted with suffix `CR` (e.g., `8,548.63 CR`).
- **Statement Header:** Always lists `PREVIOUS BALANCE` followed immediately by `PAYMENT THANK YOU - UOBT TMRW APP`.
- **Points Summary:** Includes `Points Regular Earned`, `Points Adjustment`, and `Outstanding Points Balance`.

---

## 2. Common Thai Merchant Code Dictionary

### Groceries & Convenience
| Statement Name | Real Entity | Notes |
| :--- | :--- | :--- |
| `TMN 7-11 BANGKOK` | 7-Eleven via TrueMoney | Often high frequency micro-transactions (10–150 THB) |
| `MINI BIG C -[BRANCH]` | Mini Big C convenience | Local grocery/convenience branch |
| `SUPER TURTLE PUBLIC LI` | Super Turtle convenience | Convenience store on BTS Skytrain stations |
| `TOPS-[BRANCH]` | Tops Supermarket / Food Hall | Supermarket groceries |
| `LOTUS'S [CODE] [BRANCH]` | Lotus's / Lotus's Go Fresh | Hypermarket or neighborhood store |
| `TMG MRTLATP BANGKOK` | Gourmet Market (The Mall Group) | Gourmet Market located inside MRT stations |

### Transport & Commute
| Statement Name | Real Entity | Category |
| :--- | :--- | :--- |
| `BTS [STATION] BANGKOK` | BTS Skytrain (Direct EMV contactless) | Transport |
| `BTS VISIONARY PARK` | BTS Skytrain ticketing provider | Transport |
| `MRT-BEM Bangkok TH` | MRT Blue/Purple Line (BEM) | Transport |
| `ARL. PTH. BANGKOK` | Airport Rail Link (Phaya Thai) | Transport |
| `WWW.GRAB.COM BANGKOK` | Grab (GrabBike / GrabCar / GrabFood) | Transport / Food |
| `BANGKOK EXPRESSWAY AND ME` | Expressway toll / rebate | Transport |
| `Kanchanaphisek Expressway` | Kanchanaphisek ring road toll | Transport |
| `BSRC-WONGWAEN SAHAKIJ` | Bangchak Sriracha (Esso/Bangchak fuel) | Fuel / Transport |

### Health, Fitness & Wellness
| Statement Name | Real Entity | Notes |
| :--- | :--- | :--- |
| `WWW.2C2P.COM*JETTS FIT` | Jetts Fitness 24 Hour | Monthly gym membership |
| `FITWHEY BANGKOK` | Fitwhey | Protein & workout supplements |
| `CRC SPORTS-[BRANCH]` | Supersports (Central Retail) | Athletic footwear & sports gear |

### Dining & Lifestyle
| Statement Name | Real Entity | Notes |
| :--- | :--- | :--- |
| `OHKAJHU-[BRANCH]` | Ohkajhu (สวนผักโอ้กะจู๋) | Healthy dining restaurant |
| `LPE*BEARHOUSE [BRANCH]` | Bearhouse | Milk tea / beverage shop |
| `YAMAZAKI-[BRANCH]` | Yamazaki Bakery | Japanese bakery |
| `ONE ULTRA SCREENS` | One Bangkok Cinema | Movie tickets |
| `B2S-[BRANCH]` | B2S Central | Stationery & books |
| `CENTRAL DEPT.([BRANCH])` | Central Department Store | Retail / Apparel / Tech |
| `LG ELECTRONICS TH` | LG Electronics Thailand | Appliances / Hardware |
