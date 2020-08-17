date = [
        {'id': '12234',
        'name': 'group1',
        'members_count': 1000},

        {'id': '1232234',
        'name': 'group2',
        'members_count': 1500},

        {'id': '4444',
        'name': 'group3',
        'members_count': 2000}
        ]

# dt = date[0]
# dt1 = list(dt.items())
# dt2 = [dt1[1], dt1[2]]
list3 = []
for item in date:
        name = item['name']
        members_count = item['members_count']
        list3.append((name, members_count))




print(1)
# dt = []
# for item in date:
#         dt.append({item[1]: item[2]})

print(dt)