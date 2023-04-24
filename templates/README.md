# Connects Bulk Upload Guide

## General Notes

When referring to a sheet, the same statement is also applicable to its CSV file representative. For example a statement on the Exhibition Sheet in the Excel template file is also applicable to the Exhibition.csv template file.

- All sheets and columns provided in the template must be present, even if they are not used
- `id` columns
    - Required on all sheets that have them
    - Can have any format (numeric, uuid, string, etc) and must be unique within the sheet.
    - Do not need to be _globally_ unique, so it's fine if an `Item` and an `Exhibition` can have the same identifier.
- `url` columns
    - Required for all sheets that have them
    - Must be publicly accessible `http` or `https` URLs
    - Will be downloaded and stored in our system during processing. App users will not fetch this image directly.
    - URL must change if the content changes in subsequent bulk upload. We only download a given URL one time.
- Boolean columns must  be `true` or `false`
- HTML text must be properly formatted, must be wrapped in a `<p>` tag, can only contain `<em> <strong> <a>` tags otherwise, and does not allow custom classes

## `Translation` sheets

- Used to provide translations of content in languages other than your guide's default language
- Will have subset of the fields of the "parent" sheet
- All will have `parentId` and `localeCode` fields
    - `parentId` refers to a `id` value in the parent sheet (e.g. `parentId` in `Image Translation` refers to `id` in `Image`)
    - `localeCode` refers to the language for this translation.
        - Format is `<languageCode-countryCode`.
        - Values are limited to what is supported by the Connects CMS.
        - Examples are `en-US` for US English, `fr-FR` for French, `zh-CN` for Mandarin, etc

## Sheets List

### Image

- `id` - Unique Identifier. **Required**
- `url` - URL to image file. **Required**
- `altText` - Text
- `caption` - Text

### Image Translation

- `parentId` - **Required**. Reference to Unique Identifier in `Image` sheet
- `localeCode` - **Required**. Valid and supported locale code
- `altText` - Text
- `caption` - Text

## Audio

- `id` - **Required**. Unique Identifier.
- `url` - **Required**. URL to audio file. Must be in WAV or MP3 format.
- `title` - **Required**. Text
- `description` - Text
- `transcript` - HTML Text

## Audio Translation

- `parentId` - **Required**. Reference to Unique Identifier in `Audio` sheet
- `localeCode` - **Required**. Valid and supported locale code
- `url` - **Required**. URL to audio file.  Must be in WAV or MP3 format.
- `title` - **Required** Text
- `description` - Text
- `transcript` - Text





## Creator

- `id` - **Required**. Unique Identifier
- `prefix` - Text
- `name` - **Required**. Text
- `lifedates` - Text

## Creator Translation

- `parentId` - **Required**. Reference to Unique Identifier in `Creator` sheet
- `localeCode` - **Required**. Valid and supported locale code
- `prefix` - Text
- `name` - **Required**. Text
- `lifedates` - Text


## Exhibition

- `id` - **Required**. Unique Identifier
- `title` - **Required**. **Maximum 180 characters.** Text. 
- `displayPeriod` - Boolean.
- `from` - Date in ISO format. Must be before `to` date
- `to` - Date in ISO format. Must be after `from` date
- `information` - HTML Text
- `lookupNumber` - Number. Must be unique number between 1 - 9999. Uniqueness applies across both `Exhibition` and `Item` sheets
- `itemsHeading` - Text. Default `ITEMS_IN_THIS_EXHIBITION`. Must be one of (`ITEMS_IN_THIS_EXHIBITION`, `WORKS_ON_VIEW`, `AUDIO`, `EXPLORE`, `HIGHLIGHTS`, `STOPS`)
- `displayType` - Text. Default `GRID`. Must be one of (`grid`, `list`)
- `published` - Boolean. Default `true`


## Exhibition Translation

- `parentId` - **Required**. Reference to Unique Identifier in `Exhibition` sheet
- `localeCode` - **Required**. Valid and supported locale code
- `title` - **Required**. Text.
- `information` - HTML Text

## Exhibition Image

- `exhibitionId` -  **Required**. Reference to Unique Identifier in `Exhibition` sheet
- `imageId` -  **Required**. Reference to Unique Identifier in `Image` sheet. Must be unique per `exhibitionId` in this sheet.
- `position` -  **Required**. Number, incrementing. Must be unique per `exhibitionId` in this sheet.

## Exhibition Audio

- `exhibitionId` -  **Required**. Reference to Unique Identifier in `Exhibition` sheet
- `audioId` -  **Required**. Reference to Unique Identifier in `Audio` sheet. Must be unique per `exhibitionId` in this sheet.
- `position` -  **Required**. Number, incrementing. Must be unique per `exhibitionId` in this sheet.


## Exhibition Item

- `exhibitionId` -  **Required**. Reference to Unique Identifier in `Exhibition` sheet
- `itemId` -  **Required**. Reference to Unique Identifier in `Item` sheet. Must be unique per `exhibitionId` in this sheet.
- `position` -  **Required**. Number, incrementing. Must be unique per `exhibitionId` in this sheet.

## Exhibition Related Content

NOTE: One of `toItemId` or `toExhibitId` is required. Both cannot be set.

- `fromExhibitionId` - **Required**. Reference to Unique Identifier in `Exhibition` sheet
- `toItemId` - Reference to Unique Identifier in `Item` sheet
- `toExhibitId` - Reference to Unique Identifier in `Exhibition` sheet
- `relationshipType` - **Max 180 characters**. Text
- `position` - **Required**. Number, incrementing. Must be unique per `fromExhibitionId ` in this sheet.


## Item

- `id` - **Required**. Unique Identifier
- `title` - **Required**. Text
- `creatorId` - Reference to unique identifier in `Creator` sheet
- `creationPeriod` - Text
- `materials` - Text
- `dimension` - Text
- `credit` - Text
- `accessionNumber` - Text
- `description` - Text
- `lookupNumber` - Must be unique number between 1 - 9999. Uniqueness applies across both `Exhibition` and `Item` sheets
- `published` - Boolean. Default `true`


## Item Translation

- `parentId` - **Required**. Reference to Unique Identifier in `Item` sheet
- `localeCode` - **Required**. Valid and supported locale code
- `title` - **Text**. Required
- `creationPeriod` - Text
- `materials` - Text
- `dimension` - Text
- `credit` - Text
- `accessionNumber` - Text
- `description` - Text

## Item Image

- `itemId` - **Required**. Reference to Unique Identifier in `Item` sheet
- `imageId` - **Required**. Reference to Unique Identifier in `Image` sheet. Must be unique per `itemId` in this sheet.
- `position`- **Required**. Number, incrementing. Must be unique per `itemId ` in this sheet.

## Item Audio

- `itemId` - **Required**. Reference to Unique Identifier in `Item` sheet
- `audioId` - **Required**. Reference to Unique Identifier in `Audio` sheet. Must be unique per `itemId ` in this sheet.
- `position` - **Required**. Number, incrementing. Must be unique per `itemId ` in this sheet.



## Item Related Content

- `fromItemId` - **Required**. Reference to Unique Identifier in `Item` sheet
- `toItemId` - Reference to Unique Identifier in `Item` sheet
- `toExhibitId` - Reference to Unique Identifier in `Exhibition` sheet
- `relationshipType` - Text
- `position` - **Required**. Number, incrementing. Must be unique per `fromItemId ` in this sheet. 




