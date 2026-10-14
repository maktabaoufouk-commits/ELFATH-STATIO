# EL FATH STATIO — Brand Kit « Flash & Paper »

> **Promise :** Books that hit different. Algerian, online, and in-store.
> **Idée :** un flash de phone tard sur un poche, à Alger. Pas une librairie poussiéreuse, pas une fausse bibliothèque magique.

---

## 1. Identité verrouillée

| | |
|---|---|
| **Nom (FR/EN)** | EL FATH STATIO |
| **Nom (AR)** | الفتح ستاتيو |
| **Ville** | Alger |
| **Route logo** | **Dog-ear** (marque principale : coin de page cornée + monogramme E). Le **wordmark bilingue** est utilisé pour la vitrine et l'impression. |
| **Initiale du monogramme** | E |
| **Secteur** | Librairie jeune (papeterie incluse) — en ligne + magasin |

**Livres poussés en permanence (à confirmer avec le stock réel) :**
- Auteurs algériens qu'on a *slept on* (Kamel Daoud, Kateb Yacine *Nedjma*, Amel Benmansour, Ahlam Mosteghanemi…)
- Dark romance & YA (le format qui fait vendre les stories)
- Poche à petit prix, « pas le livre de tes parents »
- fournitures / tote / marque-pages en merch

---

## 2. Voix

Court. Code-switching. Darija + français + anglais, dans la même phrase.

- « Wallah, read this. »
- « Dispo en magasin. »
- « This one stays on your nightstand. »
- « Pas le livre de tes parents. »
- « Rupture → back in stock demain inchallah. »

**Jamais :** ton institutionnel, phrases de vieux libraire, anglais de campus américain, jargon marketing générique.

---

## 3. Couleurs

| Nom | Hex | Usage |
|---|---|---|
| Ink | `#12110F` | fonds, typo, badges nuit |
| Paper | `#F3EEE4` | pages, packaging, fonds principaux |
| Olive | `#1C4A38` | le vert algérien réinterprété — **jamais plat drapeau** |
| Chili | `#E23B2F` | stickers, soldes, « NEW », marque-page |
| Saffron | `#E7A62A` | surligneur, accents |
| Signal mint | `#B8FF5C` | **social only** : « DISPO », « LIVE » |

Ratios conseillés : ~60 % paper / ~25 % ink / ~10 % olive / ~5 % chili + saffron. Le mint reste sur les réseaux.

---

## 4. Typographie

| Rôle | Famille | Graisses |
|---|---|---|
| Display latin | **Fraunces** (serif moderne à fort contraste) | 400 / 700 / 900 + italique |
| UI latin | **Inter** (grotesque propre) | 400 / 500 / 600 / 700 |
| Arabe | **Cairo** (style contemporain) | 400 / 600 / 700 / 900 |

**Règle :** toujours Latin + Arabe ensemble. Le français peut tenir la petite ligne.
Fichiers auto-hébergés dans `assets/fonts/` (SIL OFL), pas de CDN.

---

## 5. Motifs & interdits

**Motifs :** coin de page cornée · badge de notification · marque-page en bouton play · halftone / riso (pas de 3D glossy) · scènes : flash de phone, escaliers, tramway, table de café, vitrine.

**Interdits :** livres flottants, poussière magique brillante, campus américain, « pattern islamique » générique, copie cheap du drapeau en logo, néon cyberpunk, texte faux illisible.

---

## 6. Logo

### Route retenue : dog-ear

- **Marque principale** : coin de page corné + monogramme **E** (fichier vectoriel `brand/assets/logo-mark.svg`, rendu IA `brand/assets/logo-mark.png`).
- **Wordmark bilingue** pour vitrine / impression : `brand/assets/wordmark.svg` (Fraunces 900 sur Cairo 700, petite baseline olive).

### Prompts finaux (avec le vrai nom)

**Logo mark**
```text
Minimal logo mark for an Algerian Gen Z bookstore named EL FATH STATIO. A single dog-eared page corner forming a bold monogram of the letter E. Flat vector, thick geometric shapes, no gradients, no 3D, no glow, no mockup. Colors: ink black #12110F on warm paper #F3EEE4, one small chili red #E23B2F accent. Contemporary, sticker-friendly, readable at 32px. Centered on a plain background. No photorealism, no ornaments, no Arabic calligraphy flourishes, no flag, no mosque, no magic sparkles, no misspelled text, no extra letters, no watermark.
```

**Wordmark bilingue**
```text
Brand wordmark logo, flat vector. Latin text "EL FATH STATIO" in a modern high-contrast serif, stacked above Arabic text "الفتح ستاتيو" in a clean contemporary Arabic sans (Cairo style). Tight poster layout, black ink on warm paper background. Tiny olive rectangle as a baseline, no decoration. High-end independent bookstore, Algiers, youth culture, not luxury fashion, not religious, not vintage clipart. Plain background, centered, print-ready, no misspelled text, no watermark.
```

**Profile picture**
```text
App icon for a bookstore, square with slightly rounded corners. Simple dog-ear page symbol, ink black and chili red on paper cream. Extremely simple, no text, no tiny details, no mockup, no shadows, no gloss. Must stay clear as a small social profile picture.
```

**Template Stories / TikTok**
```text
Vertical 9:16 social template for an Algerian Gen Z bookstore. Warm paper texture background with subtle risograph grain. Huge empty negative space for the headline. One real paperback standing on a café table, harsh phone-flash photo, Algiers evening light, no people. Halftone dots, torn-paper edge. Colors ink, paper, olive, chili. Small sticker in the corner that says DISPO in mint on black. No magic, no floating books, no stock-library silence, no American campus, documentary not CGI, no misspelled text, no watermark.
```

**Vitrine / mockup physique**
```text
Street photo of a small independent bookstore window in Algiers, daytime, real architecture, white stairs and Mediterranean light in the background, not a landmark logo. Window vinyl: bilingual wordmark "EL FATH STATIO" and Arabic "الفتح ستاتيو", dog-ear logo, paper-cream and ink palette with one chili sticker saying "NEW". Inside: real books, a tote, a bookmark. Documentary photography, 35mm, natural, slightly grainy. No fantasy, no neon cyberpunk, no unreadable fake text, documentary not CGI.
```

**Tote + marque-page**
```text
Product photo on a concrete step: natural canvas tote bag, cream color, one-color black print of a simple dog-ear bookstore logo and the words "EL FATH STATIO". Next to it, a thick chili-red bookmark with a play-button notch. Soft daylight, phone snapshot energy, slight grain. No models, no luxury marble, no fake brand names, documentary not CGI, no misspelled text, no watermark.
```

> Note : pour les images contenant du texte, on génère d'abord le symbole / la scène seuls, puis on ajoute le vrai texte (polices réelles) dans Figma, Canva ou le HTML — comme ici.

### Exports

- Profile pic : **1080 × 1080** (PNG/SVG)
- Stories : **1080 × 1920**
- Logo vitrine : **SVG / PDF** (vectoriel)
- Texte toujours net : polices Fraunces / Inter / Cairo

---

## 7. Fichiers

```
brand/assets/logo-mark.svg      monogramme dog-ear E (vectoriel, production)
brand/assets/logo-mark.png      rendu IA (alt)
brand/assets/wordmark.svg       wordmark bilingue (vectoriel)
brand/assets/profile-pic.png    photo de profil 1024×1024
brand/assets/cover-template.png template Stories 9:16
brand/assets/window-mockup.png  vitrine Alger (vinyle ajouté en CSS)
brand/assets/tote-bookmark.png  tote + marque-page
assets/fonts/                   Fraunces · Inter · Cairo (SIL OFL)
assets/css/style.css            design system complet
index.html                      page marque vivante (téléphone d'abord)
BRAND.md                        ce document
```

---

## 8. Système social

**Six highlights** — même dog-ear, un mot chacun :
**New · Darija · FR · AR · Staff · IRL**

**Mix de contenu :**
1. 15s « ce livre en une phrase »
2. Shelf tour du magasin
3. Stories sticker « Dispo / rupture »
4. Auteurs algériens qu'on a slept on
5. Double CTA : shop the link + WhatsApp pour les commandes locales

**Une semaine de Stories :**

| Jour | Format |
|---|---|
| Lundi | Dispo / rupture (sticker) |
| Mardi | Ce livre en une phrase (15s) |
| Mercredi | Shelf tour |
| Jeudi | Auteur algérien slept on |
| Vendredi | Double CTA (link + WhatsApp) |
| Samedi | Staff pick de chevet |
| Dimanche | Vitrine IRL + NEW |

---

## 9. Dix légendes prêtes à poster

1. Wallah, read this. 📖
2. Dispo en magasin. Pas le livre de tes parents.
3. This one stays on your nightstand.
4. 15s : ce livre en une phrase. Lien en bio.
5. Rupture → back in stock demain inchallah.
6. Un auteur algérien que vous avez slept on.
7. FR + AR sur la même étagère. Comme ça.
8. On l'a lu. On l'a kiffé. Viens.
9. Café + paperback + soirée à Alger. That's it.
10. WhatsApp pour commander local, link pour le reste.

---

## 10. À remplacer avant le lancement

- Liens réels : WhatsApp, boutique en ligne, réseaux (actuellement des ancres `#cta` / `#top`)
- Adresse et horaires du magasin (footer)
- Liste réelle des livres poussés + prix
- Comptes sociaux réels (@elfath.statio est un placeholder)
