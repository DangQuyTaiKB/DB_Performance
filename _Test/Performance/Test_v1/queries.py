import requests
import json
from time import perf_counter
import asyncio

queries = {
    "rolecategories": {
        "readp": '{ result: roleCategoryPage { __typename, id, name, nameEn}}',
        "read": 'query ($id: UUID!) { result: roleCategoryById(id: $id) { __typename, id, name, nameEn }}',
        "create": '''
            mutation($id: UUID!, $name: String!, $name_en: String) {
                result: roleCategoryInsert(roleCategory: {id: $id, name: $name, nameEn: $name_en}) {
                    id
                    msg
                    result: roleCategory {
                        id
                        lastchange
                    }
                }
            }
        '''
    },

    "roletypes":{
        "readp": '{ result: roleTypePage { __typename, id, name, nameEn}}',
        "read": 'query ($id: UUID!) { result: roleTypeById(id: $id) { __typename, id, name, nameEn }}',
        "create": '''
            mutation($id: UUID!, $name: String!, $name_en: String) {
                result: roleTypeInsert(roleType: {id: $id, name: $name, nameEn: $name_en}) {
                    id
                    msg
                    result: roleType {
                        id
                        lastchange
                    }
                }
            }
        '''
    },

    "grouptypes": {
        "readp": '{ result: groupTypePage { __typename, id, name, nameEn}}',
            "read": 'query ($id: UUID!) { result: groupTypeById(id: $id) { __typename, id, name, nameEn}}',
            "create": '''
                mutation($id: UUID!, $name: String!, $name_en: String) {
                result: groupTypeInsert(groupType: {id: $id, name: $name, nameEn: $name_en}) {
                    id
                    msg
                    result: groupType {
                        id
                        lastchange
                    }
                }
            }'''

    },

    "groups": {
        "readp": '{ result: groupPage { __typename, id, name, nameEn}}',
        "read": 'query ($id: UUID!) { result: groupById(id: $id) { __typename, id, name, nameEn}}',
        "create": '''
            mutation($id: UUID!, $grouptype_id: UUID!, $mastergroup_id: UUID, $name: String!, $name_en: String) {
            result: groupInsert(group: {id: $id, name: $name, nameEn: $name_en, grouptypeId: $grouptype_id, mastergroupId: $mastergroup_id}) {
                id
                msg
                result: group {
                    id
                    lastchange
                }
            }
        }'''

    },

    "users": {
        "readp": '{ result: userPage { __typename, id, name, surname, email}}',
        "read": 'query ($id: UUID!) { result: userById(id: $id) { __typename, id, name, surname, email}}',
        "create": '''
            mutation($id: UUID!, $name: String!, $surname: String!, $email: String!) {
            result: userInsert(user: {id: $id, name: $name, surname: $surname, email: $email}) {
                id
                msg
                result: user {
                    id
                    lastchange
                }
            }
        }'''
    },

    "memberships": {
        "readp": '{ result: membershipPage { __typename, id, valid }}',
        "read": 'query ($id: UUID!) { result: membershipById(id: $id) { __typename, id, valid}}',
        "create": '''
            mutation($id: UUID!, $user_id: UUID!, $group_id: UUID!, $valid: Boolean) {
            result: membershipInsert(membership: {id: $id, userId: $user_id, groupId: $group_id, valid: $valid}) {
                id
                msg
                result: membership {
                    id
                    lastchange
                }
            }
            }'''                        
        },

    "formsections": {
        "read": 'query($id: UUID!){ result: formSectionById(id: $id) { id }}',
        "create": '''
            mutation ($id: UUID!, $name: String!, $order: Int!, $name_en: String!, $form_id: UUID!) {
                formSectionInsert(
                    section: {id: $id, name: $name, order: $order, nameEn: $name_en, formId: $form_id}
                )
                {
                    id
                    msg
            }
        }'''
    },

    
    "formparts":{
        "read": 'query($id: UUID!){ result: formPartById(id: $id) { id }}',
        "create": '''
            mutation ($id: UUID!, $name: String!, $order: Int!, $name_en: String!, $section_id: UUID!) {
                formPartInsert(part: {id: $id, name: $name, order: $order, nameEn: $name_en, sectionId: $section_id}) 
                {
                    id
                    msg
                }
        }'''
    },

    "formitems": {
        "read": 'query($id: UUID!){ result: formItemById(id: $id) { id }}',
        "create": '''
            mutation ($id: UUID!, $name: String!, $order: Int!, $name_en: String!, $part_id: UUID!) {
                formItemInsert(item: {id: $id, name: $name, order: $order, nameEn: $name_en, partId: $part_id}) 
                {
                    id
                    msg
                }
        }'''
    },

    "formrequests": {
        "read": 'query($id: UUID!){ result: requestById(id: $id) { id }}',
        "create": '''
            mutation ($id: UUID!, $name: String!) {
                formRequestInsert(request: {id: $id, name:$name }) 
            {
                id
                msg
            }
        }'''
    },

    

}