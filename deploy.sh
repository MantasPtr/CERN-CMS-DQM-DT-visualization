# git clone git@github.com:MantasPtr/CERN-CMS-DQM-DT-visualization.git

# python 3.6
sudo yum install -y python36
# pip for python 3.6
curl https://bootstrap.pypa.io/get-pip.py | sudo  python36
#python dependencies
sudo python36 -m pip install flask pymongo aiohttp tensorflow keras scikit-image sklearn

# adding mongo if it was not added before repository
MONGO_REPO=/etc/yum.repos.d/mongodb-org-4.0.repo
if [ ! -f $MONGO_REPO ] || ! grep -Fxq "baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/4.0/x86_64/" $MONGO_REPO
then
cat << EOT >> $MONGO_REPO 
[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
EOT
fi

# install mongo 4 
sudo yum install -y mongodb-org
# start mongo
sudo service mongod start

# open port 8080 
sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT
# redirect port 80 to 8080
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080