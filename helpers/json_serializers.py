from connectivity.models import Profile, CriminalCode, CriminalRecord
from django.db.models import QuerySet
from logging import getLogger


logger = getLogger()


def get_profiles_and_criminal_data_dict(profiles: QuerySet[Profile]):
    data_dict = {"profiles_batch": []}
    for profile in profiles:
        try:
            criminal_records = CriminalRecord.objects.filter(profile=profile)
        except CriminalRecord.DoesNotExist as e:
            logger.exception(e)
            raise e
        criminal_record_dicts = []
        for criminal_record in criminal_records:
            criminal_record_dict = {
                "code": criminal_record.criminal_code_record.code,
                "name": criminal_record.criminal_code_record.name,
                "description": criminal_record.description
            }
            criminal_record_dicts.append(criminal_record_dict)
        profile_dict = {
            "id": profile.id,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "birth_date": profile.birth_date,
            "place_of_residence": profile.place_of_residence,
            "criminal_record": criminal_record_dicts
        }
        data_dict["profiles_batch"].append(profile_dict)
    return data_dict
