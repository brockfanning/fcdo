const path = require('path')
const mammoth = require('mammoth')
const cheerio = require('cheerio')
const { Metadata, WordTemplateOutput } = require('sdg-metadata-convert')
const wordTemplateOutput = new WordTemplateOutput()
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
    //'global_indicator_description',
    //'un_designated_tier',
    //'un_custodian_agency',
    //'link_to_un_metadata',
    'source_organization',
    'data_source',
    'reporting_source',
    'reporting_organization',
    'source_organization_1',
    'periodicity',
    'earliest_available_data',
    'link_to_data source_the_text_to_show_instead_of_the_url',
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
        'SDG_CUSTODIAN_AGENCIES': ``,
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
        `,
        'OTHER_DOC': `
            {% if other_information %}
            <h2>Other information</h2>
            {{ other_information }}
            {% endif %}
        `,
    }
}

mammoth.convertToHtml({path: 'web/_data/countries/rwanda/77 Metadata document.docx'})
    .then(function(result) {
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
            }

            const templates = getConceptTemplates()
            const newMetadata = {}
            for (const key of Object.keys(templates)) {
                const rendered = nunjucks.renderString(templates[key], oldMetadata).trim()
                newMetadata[key] = rendered
            }
            const metadata = new Metadata(newMetadata)

            const folder = path.join('web', '_data', 'countries', 'rwanda', 'metadata-templates')
            const filename = indicatorId.replace(/\./g, '-') + '.docm'
            const filepath = path.join(folder, filename)
            wordTemplateOutput.write(metadata, filepath)
                .then(() => console.log(`Created ${filepath}.`))
                .catch(err => console.log(err))
        }
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