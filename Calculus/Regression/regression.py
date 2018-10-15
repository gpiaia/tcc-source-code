from apm import *

s = 'http://byu.apmonitor.com'
a = 'regression'

apm(s,a, 'clear_all')

apm_load(s, a, 'model.apm')
csv_load(s, a, 'data.csv')

apm_info(s,a,'FV', 'ts')
apm_info(s,a,'FV', 'qsi')

apm_option(s, a, 'qsi.status',1)
apm_option(s, a, 'ts.status',1)

apm_option(s, a, 'nlc.inode',2)

output = apm(s,a,'solve')
print(output)
#*(cos((x/ts)*sqrt(1-qsi^2))+(qsi/(sqrt(1-qsi^2)))*sin((x/ts)*sqrt(1-qsi^2))))
