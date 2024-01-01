redis-cli flushall
sudo mysql -Nse 'show tables' cgrates | while read table; do sudo mysql -e "truncate table $table" cgrates; done
cgr-migrator -exec=*set_versions -stordb_passwd=CGRateS.org
sudo systemctl restart cgrates
