const path = require('path')
const mammoth = require('mammoth')
const cheerio = require('cheerio')
const { Metadata, WordTemplateOutput, SdmxOutput, descriptorStore } = require('sdg-metadata-convert')
const wordTemplateOutput = new WordTemplateOutput({
    template: path.join('scripts', 'templates', 'SDG_Metadata_Template_Rwanda.docm'),
})
const sdmxOutput = new SdmxOutput()
const nunjucks = require('nunjucks')
nunjucks.configure({ autoescape: false });

// This file builds the Rwanda templates.

const validMetadataFields = [
    'definition',
    'geographic_coverage',
    'geographical_coverage',
    'unit_of_measurement',
    'computation_method',
    'disaggregation',
    'comments_and_limitations_other_information',
    'indicator_name',
    'indicator_number',
    'target_name',
    'target_number',
    'global_indicator_description',
    'un_designated_tier',
    'un_custodian_agency',
    'link_to_un_metadata',
    'source_organization',
    'data_source',
    'reporting_source',
    'reporting_organization',
    'source_organization_1',
    'periodicity',
    'earliest_available_data',
    'link_to_data_source_the_text_to_show_instead_of_the_url',
    'release_date',
    'next_release_date',
    'statistical_classification',
    'contact_details',
    'other_information',
    'available_indicator',
    'indicator_available',
]

function getConceptTemplates() {
    return {
        'SDG_INDICATOR_INFO': ``,
        'SDG_GOAL': ``,
        'SDG_TARGET': `
            {{ target_number }} {{ target_name }}
        `,
        'SDG_INDICATOR': `
            {{ indicator_number }} {{ indicator_name }}
        `,
        'SDG_SERIES_DESCR': ``,
        'META_LAST_UPDATE': `
            {{ release_date }}
        `,
        'SDG_RELATED_INDICATORS': ``,
        'SDG_CUSTODIAN_AGENCIES': `
            {{ un_custodian_agency }}
        `,
        'CONTACT': ``,
        'CONTACT_ORGANISATION': `
            {{ source_organization }}
        `,
        'CONTACT_NAME': ``,
        'ORGANISATION_UNIT': ``,
        'CONTACT_FUNCT': ``,
        'CONTACT_PHONE': ``,
        'CONTACT_MAIL': ``,
        'CONTACT_EMAIL': `
            {{ contact_details }}
        `,
        'IND_DEF_CON_CLASS': ``,
        'STAT_CONC_DEF': `
            {{ definition }}
        `,
        'UNIT_MEASURE': `
            {{ unit_of_measurement }}
        `,
        'CLASS_SYSTEM': `
            {{ statistical_classification }}
        `,
        'SRC_TYPE_COLL_METHOD': ``,
        'SOURCE_TYPE': ``,
        'COLL_METHOD': ``,
        'FREQ_COLL': `
            {{ periodicity }}
        `,
        'REL_CAL_POLICY': `
            {% if next_release_date %}
            <h2>Next release date</h2>
            {{ next_release_date }}
            {% endif %}
        `,
        'DATA_SOURCE': `
            {{ data_source }}
            {{ source_the_text_to_show_instead_of_the_url }}
        `,
        'COMPILING_ORG': `
            {{ reporting_organization }}
        `,
        'INST_MANDATE': ``,
        'OTHER_METHOD': ``,
        'RATIONALE': ``,
        'REC_USE_LIM': `
            {{ comments_and_limitations_other_information }}
        `,
        'DATA_COMP': `
            {{ computation_method }}
        `,
        'DATA_VALIDATION': ``,
        'ADJUSTMENT': ``,
        'IMPUTATION': ``,
        'REG_AGG': ``,
        'DOC_METHOD': ``,
        'QUALITY_MGMNT': ``,
        'QUALITY_ASSURE': ``,
        'QUALITY_ASSMNT': ``,
        'COVERAGE': `
            {% if earliest_available_data %}
            <h2>Earliest available data</h2>
            {{ earliest_available_data }}
            {% endif %}

            {% if geographical_coverage or geographic_coverage %}
            <h2>Geographical coverage</h2>
            {{ geographical_coverage }} {{ geographic_coverage }}
            {% endif %}

            {% if disaggregation %}
            <h2>Disaggregation</h2>
            {{ disaggregation}}
            {% endif %}
        `,
        'COMPARABILITY': `
            {% if available_indicator or indicator_available %}
            <h2>Indicator available</h2>
            {{ available_indicator }}
            {{ indicator_available }}
            {% endif %}

            {% if global_indicator_description %}
            <h2>Global indicator description</h2>
            {{ global_indicator_description }}
            {% endif %}

            {% if link_to_un_metadata %}
            <h2>Link to UN Metadata</h2>
            {{ link_to_un_metadata }}
            {% endif %}

        `,
        'OTHER_DOC': `
            {% if other_information %}
            <h2>Other information</h2>
            {{ other_information }}
            {% endif %}

            {% if un_designated_tier %}
            <h2>UN designated tier</h2>
            {{ un_designated_tier }}
            {% endif %}
        `,
    }
}

const originalFields = {}

function prepareOutput(text) {
    return text
        .replace(/'/g, '&#39;')
}

function getSeriesFromIndicatorId(indicatorId) {
    indicatorId = indicatorId.replace(/-/g, '.')
    const series = descriptorStore.getDescriptor('SERIES')
    const matches = series.options.filter(item => item.indicatorIds.includes(indicatorId))
    return (matches.length === 0) ? false : matches.map(match => match.key)
}

mammoth.convertToHtml({path: 'web/_data/countries/rwanda/77 Metadata document.docx'})
    .then(async function(result) {
        const html = result.value
        const messages = result.messages
        const $ = cheerio.load(html)
        for (const h2 of $('body > h2')) {
            const text = $(h2).text().trim()
            if (!isIndicatorTitle(text)) {
                continue
            }
            const indicatorId = getIndicatorId(text)
            const table = $(h2).next('table')

            const oldMetadata = {}

            for (const row of $(table).find('tbody > tr')) {
                const cells = $(row).find('> td')
                if (cells.length < 2) {
                    continue
                }
                const field = normalizeField($(cells[0]).text())
                if (validMetadataFields.includes(field) === false) {
                    continue
                }

                const value = $(cells[1]).html().trim()
                if (value === '') {
                    continue
                }
                oldMetadata[field] = value
                originalFields[field] = $(cells[0]).text()
            }

            const templates = getConceptTemplates()
            const newMetadata = {}
            for (const key of Object.keys(templates)) {
                const rendered = nunjucks.renderString(templates[key], oldMetadata).trim()
                newMetadata[key] = prepareOutput(rendered)
            }

            const series = getSeriesFromIndicatorId(indicatorId)
            const descriptors = {
                'LANGUAGE': 'en',
                'REPORTING_TYPE': 'N',
                'REF_AREA': 'RW',
                'SERIES': series,
            }

            const metadata = new Metadata(newMetadata, descriptors)

            const folder = path.join('web', '_site', 'rwanda')
            const filename = indicatorId.replace(/\./g, '-') + '.docm'
            const filepath = path.join(folder, filename)
            await wordTemplateOutput.write(metadata, filepath)
                .then(() => console.log(`Created ${filepath}.`))
                .catch(err => console.log(err))

            if (!series) {
                console.log('Unable to produce SDMX for ' + indicatorId + '. SERIES could not be identified.')
            }
            else {
                const sdmxPath = path.join(folder, filename.replace('.docm', '.xml'))
                await sdmxOutput.write(metadata, sdmxPath)
                    .then(() => console.log(`Created ${sdmxPath}.`))
                    .catch(err => console.log(err))
            }

        }
        //console.log(originalFields)
    })
    .done();

function isIndicatorTitle(text) {
    const first = text.split(' ')[0]
    return isIndicatorId(first)
}

function isIndicatorId(text) {
    const parts = text.split('.')
    return parts.length === 3
}

function getIndicatorId(text) {
    return text.split(' ')[0]
}

function normalizeField(field) {
    return field
        .trim()
        .toLowerCase()
        .replace(/ /g, '_')
        .replace(/\//g, '')
        .replace(/\-/g, '_')
        .trim()
}