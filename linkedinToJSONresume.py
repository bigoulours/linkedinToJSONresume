# This function creates a JSON-Resume from a any LinkedIn profile
# The arguments are profile, skills and contact info as provided by linkedin-api (https://github.com/tomquirk/linkedin-api):
def linkedin_to_json_resume(linkedin_profile_object, linkedin_skills, contact_info):
    json_resume = dict()
    json_resume['basics'] = dict()
    json_resume['basics']['name'] = linkedin_profile_object['firstName'] + ' ' + linkedin_profile_object['lastName']
    json_resume['basics']['label'] = linkedin_profile_object['headline']
    if 'displayPictureUrl' in linkedin_profile_object.keys():
        json_resume['basics']['image'] = linkedin_profile_object['displayPictureUrl'] + linkedin_profile_object['img_200_200']
    else:
        json_resume['basics']['image'] = ""

    if contact_info['email_address'] is not None:
        json_resume['basics']['email'] = contact_info['email_address']
    if len(contact_info['phone_numbers']) > 0:
        nb_list = [x['number'] for x in contact_info['phone_numbers']]
        json_resume['basics']['phone'] = ' / '.join(nb_list)

    for website in contact_info['websites']:
        if website['label'] != 'COMPANY' and \
                not (any([x in website['url']
                     for x in ['github.com', 'twitter.com', 'gitlab.com']])):   # those are added under "profiles"
            json_resume['basics']['website'] = website['url']
            break

    if 'summary' in linkedin_profile_object.keys():
        json_resume['basics']['summary'] = linkedin_profile_object['summary']

    json_resume['basics']['location'] = dict()
    if 'geoLocationName' in linkedin_profile_object.keys():
        json_resume['basics']['location']['city'] = linkedin_profile_object['geoLocationName']
    if 'location' in linkedin_profile_object.keys() and 'basicLocation' in linkedin_profile_object['location'].keys():
        if 'postalCode' in linkedin_profile_object['location']['basicLocation'].keys():
            json_resume['basics']['location']['postalCode'] = linkedin_profile_object['location']['basicLocation']['postalCode']
        if 'countryCode' in linkedin_profile_object['location']['basicLocation'].keys():
            json_resume['basics']['location']['countryCode'] = linkedin_profile_object['location']['basicLocation']['countryCode'].upper()


    # todo add social network profiles (github, twitter, gitlab...) from websites urls
    # todo add instant messenger profiles (skype, ICQ, WeChat...)

    json_resume['work'] = []
    for exp in linkedin_profile_object['experience']:
        json_exp = dict()
        json_exp['company'] = exp['companyName']    # old schema version
        json_exp['name'] = exp['companyName']       # new schema version
        json_exp['position'] = exp['title']
        if 'locationName' in exp.keys():
            json_exp['location'] = exp['locationName']
        json_exp['startDate'] = str(exp['timePeriod']['startDate']['year']) + '-' + str(exp['timePeriod']['startDate']['month']).zfill(2)
        if 'endDate' in exp['timePeriod'].keys():
            json_exp['endDate'] = str(exp['timePeriod']['endDate']['year']) + '-' + str(exp['timePeriod']['endDate']['month']).zfill(2)
        if 'description' in exp.keys():
            json_exp['highlights'] = []
            for highlight in exp['description'].split('\n'):
                if highlight != "":
                    json_exp['highlights'].append(highlight)
        json_resume['work'].append(json_exp)

    json_resume['education'] = []
    for edu in linkedin_profile_object['education']:
        json_edu = dict()
        json_edu['institution'] = edu['schoolName']
        if 'fieldOfStudy' in edu.keys():
            json_edu['area'] = edu['fieldOfStudy']
        if 'degreeName' in edu.keys():
            json_edu['studyType'] = edu['degreeName']
        if 'timePeriod' in edu.keys():
            if 'startDate' in edu['timePeriod'].keys():
                json_edu['startDate'] = str(edu['timePeriod']['startDate']['year'])
            if 'endDate' in edu['timePeriod'].keys():
                json_edu['endDate'] = str(edu['timePeriod']['endDate']['year'])
        else:
            json_edu['endDate'] = ""
        json_resume['education'].append(json_edu)

    json_resume['volunteer'] = []
    for vol in linkedin_profile_object['volunteer']:
        json_vol = dict()
        json_vol['organization'] = vol['companyName']
        if 'role' in vol.keys():
            json_vol['position'] = vol['role']
        if 'timePeriod' in vol.keys():
            if 'startDate' in vol['timePeriod'].keys():
                json_vol['startDate'] = str(vol['timePeriod']['startDate']['year'])
            if 'endDate' in vol['timePeriod'].keys():
                json_vol['endDate'] = str(vol['timePeriod']['endDate']['year'])
        if 'cause' in vol.keys():
            json_vol['summary'] = vol['cause'].replace('_', ' ')
        if 'description' in vol.keys():
            json_vol['highlights'] = []
            for highlight in vol['description'].split('\n'):
                if highlight != "":
                    json_vol['highlights'].append(highlight)
        json_resume['volunteer'].append(json_vol)

    json_resume['awards'] = []
    for award in linkedin_profile_object['honors']:
        json_award = dict()
        json_award['title'] = award['title']
        if 'issueDate' in award.keys():
            if 'year' in award['issueDate'].keys():
                json_award['date'] = str(award['issueDate']['year'])
                if 'month' in award['issueDate'].keys():
                    json_award['date'] = json_award['date'] + '-' + str(award['issueDate']['month']).zfill(2)
        if 'issuer' in award.keys():
            json_award['awarder'] = award['issuer']
        if 'description' in award.keys():
            json_award['summary'] = award['description']
        json_resume['awards'].append(json_award)

    json_resume['publications'] = []
    for pub in linkedin_profile_object['publications']:
        json_pub = dict()
        json_pub['name'] = pub['name']
        if 'publisher' in pub.keys():
            json_pub['publisher'] = pub['publisher']
        if 'date' in pub.keys():
            if 'year' in pub['date'].keys():
                json_pub['releaseDate'] = str(pub['date']['year'])
                if 'month' in pub['date'].keys():
                    json_pub['releaseDate'] = json_pub['releaseDate'] + '-' + str(pub['date']['month']).zfill(2)
        if 'url' in pub.keys():
            json_pub['website'] = pub['url']
        if 'description' in pub.keys():
            json_pub['summary'] = pub['description']
        json_resume['publications'].append(json_pub)

    json_resume['skills'] = []
    json_skills = dict()
    json_skills['name'] = 'Skills'
    json_skills['keywords'] = [x['name'] for x in linkedin_skills]
    json_resume['skills'].append(json_skills)

    # # old json-resume schema
    # if linkedin_profile_object['certifications']:
    #   json_certif = dict()
    #   json_certif['name'] = 'Certifications'
    #   json_certif['keywords'] = [x['name'] for x in linkedin_profile_object['certifications']]
    #   json_resume['skills'].append(json_certif)

    # # new json-resume schema
    json_resume['certificates'] = []
    for certif in linkedin_profile_object['certifications']:
        json_certif = dict()
        json_certif['name'] = certif['name']
        json_certif['issuer'] = certif['authority']
        if 'timePeriod' in certif.keys():
            json_certif['date'] = str(certif['timePeriod']['startDate']['year'])
            if 'month' in certif['timePeriod']['startDate'].keys():
                json_certif['date'] += "-" + str(certif['timePeriod']['startDate']['month']).zfill(2)
        json_resume['certificates'].append(json_certif)

    json_resume['languages'] = []
    for lang in linkedin_profile_object['languages']:
        json_lang = dict()
        json_lang['language'] = lang['name']
        if 'proficiency' in lang.keys():
            json_lang['fluency'] = lang['proficiency'].lower().replace('_', ' ')
        json_resume['languages'].append(json_lang)

    # todo: interests?, references?, birthday?

    return json_resume


if __name__ == "__main__":
    # getting logged user resume when called as main
    from linkedin_api import Linkedin
    import getpass
    import json
    print("Please enter your LinkedIn credentials first (2FA must be disabled)")
    username = input("user: ")
    password = getpass.getpass('password: ')
    try:
        api = Linkedin(username, password)
    except:
        print("Login failed! Check your credentials (and disable 2FA if needed)")
        quit()
    my_mini_profile = api.get_user_profile()['miniProfile']
    my_public_id = my_mini_profile['publicIdentifier']
    my_profile = api.get_profile(public_id=my_public_id)
    my_skills = api.get_profile_skills(public_id=my_public_id)
    my_contact_info = api.get_profile_contact_info(public_id=my_public_id)
    my_profile_as_json_resume = linkedin_to_json_resume(my_profile, my_skills, my_contact_info)
    print(json.dumps(my_profile_as_json_resume, indent=4))

