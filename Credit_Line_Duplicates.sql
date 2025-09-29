SELECT
    hp.party_name, --customer party name
    hpa.OVERALL_CREDIT_LIMIT, --total site credit limit
    hpa.CURRENCY_CODE, --currency
    hpa.CREATION_DATE, --creation of credit line date
    hp.party_name AS Company_Name,
    hca.account_number, --customer account number
    hps.party_site_number AS SITE_NUMBER, --customer site number
    hl.country, --customer site country
    hl.address1, --customer site address line 1
    hl.address2, --customer site address line 2
    hl.address3, --customer site address line 3
    hl.address4, --customer site alternate name
    hl.city, --customer site city
    hl.postal_code, --customer site postal code
    hl.state, --customer site state DISABLE FOR CANADA
    --hl.province, --customer site provence ENABLE FOR CANADA
    hl.county, --customer site county
    hl.content_source_type, --customer site USER created OR DATA conversion created
    hSU.LOCATION, --customer site CITY-EC-SITENUMBER NOT sure what this IS CALLED though
    hcasa.orig_system_reference AS site_orig_system_reference, --customer OU EC EC# bill TO AND P21(????)
    hl.actual_content_source, --user vs dataload entry
	hps.location_id, --locations id used for testing
    hsu.cust_acct_site_id --site id used for testing
    --hou.name AS operting_unit_name, --Manually set below for TCS
    --hp.party_number, --THE REST OF THESE ARE SORT OF IRRELEVENT BUT HELP WITH THE SELECTIONS ALTHOUGH I CANNOT FIND A USE FOR ADDING THEM
    --hSU.SITE_USE_CODE, --customer site use: bill to, ship to, sold to (Manually set for  'Bill to' below)
    --hcasa.attribute1, --customer site ownership (Manually set for 'Trane Commercial (EC)' below)
    --hl.orig_system_reference, --customer site reference NUMBER (THIS IS NOT THE SITE NUMBER!!!)
    --hps.identifying_address_flag, --set for collectionsn queue
FROM
    ar.hz_locations hl, --pulling FROM AR SCHEMA TABLE: HZ_LOCATIONS, saving TABLE AS hl FOR query
    ar.hz_party_sites hps, --pulling FROM AR SCHEMA TABLE: HZ_PARTY_SITES, saving TABLE AS hps FOR query
    ar.hz_cust_acct_sites_all hcasa, --pulling FROM AR SCHEMA TABLE: HZ_CUST_ACCT_SITES_ALL, saving TABLE AS hcasa FOR query
    ar.hz_parties hp, --pulling FROM AR SCHEMA TABLE: HZ_PARTIES, saving TABLE AS hp FOR query
    ar.hz_cust_accounts hca, --pulling FROM AR SCHEMA TABLE: HZ_CUST_ACCOUNTS, saving TABLE AS hca FOR query
    hr_operating_units hou, --NOT sure how this one IS pulling... yet
    ar.HZ_CUST_SITE_USES_ALL hsu, --pulling FROM AR SCHEMA TABLE: HZ_CUST_SITE_USES_ALL, saving TABLE AS su FOR query
    AR.HZ_CUST_PROFILE_AMTS hpa -- puling from ar schema table: HZ_CUST_PROFILE_AMTS
WHERE
    hpa.cust_account_id = hcasa.cust_account_id --Match rule for account and credit
    AND hpa.SITE_USE_ID = hsu.SITE_USE_ID --Match rule for site and credit
    AND hcasa.org_id = hou.organization_id --MATCH rule FOR: org id (limits to single entries)
    AND hp.party_type = 'ORGANIZATION' --MATCH rule FOR: org
    AND hps.status = 'A' --MATCH rule FOR: active
    AND hcasa.status = 'A' --MATCH rule FOR: active
    AND hp.status = 'A' --MATCH rule FOR: active
    AND hca.status = 'A' --MATCH rule FOR: active
    AND hSU.SITE_USE_CODE = 'BILL_TO' --only sites with active credit
    AND hl.COUNTRY = 'US' --limited to US to prevent server throttling
    AND hou.name = 'US OU USD TCS' --limited to US USD TCS to prevent server throttling
    AND hcasa.attribute1 = 'Trane Commercial (EC)' --only accounts that credit matters on
    --AND hps.party_site_number = '306135'
	--AND hSU.LOCATION LIKE ('%OVERLAND PARK - 3455716-306135%')
	AND hpa.CUST_ACCOUNT_ID = hcasa.CUST_ACCOUNT_ID
    AND hcasa.party_site_id = hps.party_site_id --MATCH rule FOR: matching customer account site party id WITH party
    AND hps.location_id = hl.location_id --MATCH rule FOR: matching party location id WITH site location id
    AND hp.party_id = hca.party_id --MATCH rule FOR: XREF LINES
    AND hp.party_id = hps.party_id --MATCH rule FOR: XREF LINES;
