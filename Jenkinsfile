def CHEF_WORKSTATION='CHEF-WORKSTATION'
def App01NodeADev19 = 'App01NodeADev19'
def App01NodeBDev19 = 'App01NodeBDev19'
def App02NodeADev19 = 'App02NodeADev19'
def App02NodeBDev19 = 'App02NodeBDev19'
def IDMNodeADev19 = 'IDMNodeADev19'
def IDMNodeBDev19 = 'IDMNodeBDev19'
def DBDev19 = 'DBDev19'

pipeline {
	agent none

	parameters {
		string (name: 'ENV_NAME', defaultValue: 'Dev19', description: 'Which environment to be used ?')
		string (name : 'HOST_LIST', defaultValue:'hostlist_dev_2', description: 'File name for the hostlist ?')
		string (name : 'HA', defaultValue:'false',description:'HA true/false ?')
		string (name : 'DBCONTAINER', defaultValue:'cdb882',description:'Container DB Name ?')
		string (name : 'DBPLUGGABLE', defaultValue:'pdb882',description:'Pluggable DB Name ?')
	}

	options {
		timestamps()
		
	}
	
	stages {
	
		stage('Tagging the nodes with stop_server tag'){
			agent{
				node{
					label "${CHEF_WORKSTATION}"
				}
			}
			steps{
				script {
					try{
						sh '''
							echo "Coldplay@123" | sudo -S /u01/workstation/chef-repo/knife_tag_assign_role.sh /u01/workstation/chef-repo/${HOST_LIST} stop_servers "recipe[pgbu_reboot_new::stop_servers_V7]"	
							echo $pwd
						'''
					}
					catch(Exception e){
						sh '''
							echo 'Unable to tag stop_servers'
						'''
						throw e
					}
				}
			}
		}
		
		stage('Stopping servers in App01, App02 , IDM'){
			parallel {
				stage('App01NodeA'){
					agent {
						label "${App01NodeADev19}"
					}
					
					steps {
						sh '''
							//cd /tmp
							//chef-client -l debug -L stopServer.log
							echo "running stop server chef-client in App01NodeA"
						'''
						script {
							try{
								sh'''
									//ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
									echo "Killing /u01 processes in App01NodeA"
								'''
							}catch(Exception e){
								throw e
							}
						}
					}
				}
				
				stage('App02NodeA'){
					agent {
						label "${App02NodeADev19}"
					}
					
					steps {
						sh '''
							//cd /tmp
							//chef-client -l debug -L stopServer.log
							echo "running stop server chef-client in App02NodeA"
						'''
						script{
							try{
								sh'''
									//ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
									echo "Killing /u01 processes in App02NodeA"
								'''
							}catch(Exception e){
								throw e
							}
						}
					}
				}
				
				stage('IDMNodeA'){
					agent {
						label "${App01NodeADev19}"
					}
					
					steps {
						sh '''
							//cd /tmp
							//chef-client -l debug -L stopServer.log
							echo "running stop server chef-client in IDMNodeA"
						'''
						
						script {
							try{
								sh'''
									//ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
									echo "Killing /u01 processes in IDMNodeA"
								'''
							}catch(Exception e){
								throw e
							}
						}
					}
				}
				
				stage('App01NodeB'){
					agent {
						label "${App01NodeBDev19}"
					}
					steps {
						when (expression { ${HA}==true}){
							sh '''
								//cd /tmp
								//chef-client -l debug -L stopServer.log
								echo "running stop server chef-client in IDMNodeA"
							'''
							script {
								try{
									sh'''
										//ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
										echo "Killing /u01 processes in App01NodeB"
									'''
								}catch(Exception e){
									throw e
								}
							}
						}
					}
				}
					
				stage('App02NodeB'){
					agent {
						label "${App01NodeBDev19}"
					}
					steps {
						when (expression { ${HA}==true}){
							sh '''
								//cd /tmp
								//chef-client -l debug -L stopServer.log
								echo "running stop server chef-client in App02NodeB"
							'''
							script{
								try{
									sh'''
										//ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
										echo "Killing /u01 processes in App02NodeB"
									'''
								}catch(Exception e){
									throw e
								}
							}
						}
					}
				}
					
				stage('IDMNodeB'){
					agent {
						label "${IDMNodeBDev19}"
					}
					steps{
						when (expression { ${HA}==true}){
							sh '''
								//cd /tmp
								//chef-client -l debug -L stopServer.log
								echo "running stop server chef-client in IDMNodeB"
							'''
							script {		
								try{
									sh'''
										//ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
										echo "Killing /u01 processes in IDMNodeB"
									'''
								}catch(Exception e){
									throw e
								}
							}
						}
					}
				}
			}
		}
		
		stage('Stopping database'){ 
			agent {
				label "${DBDev19}"
			}
			steps{
				sh'''
					//cd /u01/
					//rm -rf stopDB.py   || true
					//wget "http://kkm00bme.in.oracle.com:8080/job/Cloud_Automation_BATS/ws/stopDB.py"
					//sudo -H -u gbuora python stopDB.py ${DBCONTAINER} ${DBPLUGGABLE} /u01/app/oracle/
					echo "Stopping database"
				'''
				script {
					try{
						sh'''
							//ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
							echo "Killing /u01 processes in DB"
						'''
						}catch(Exception e){
							throw e
						}
				}
			}
		}
		
		stage ('Taking backup'){
			parallel{
				stage('DB Backup'){
					agent {
						label "${DBDev19}"
					}
					steps{
						script{
							try{
								sh'''
									//rm -rf /u02/Backup/DB.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
							
						sh'''
							//cd /u01
							//tar -cvf /u02/Backup/DB.tar.gz app
							echo "Taking db backup"
						'''
					}
				}
				
				stage('App01NodeA Backup'){
					agent {
						label "$App01NodeADev19"
					}
					steps{
						script{	
							try{
								sh'''
									//rm -rf /u02/Backup/App01NodeA.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
						sh'''
							//cd /u01
							//tar -cvf /u02/Backup/App01NodeA.tar.gz app
							echo "taking backup app01NodeA"
						'''
					}
				}
				
				stage('App02NodeA Backup'){
					agent {
						label "$App02NodeADev19"
					}
					steps{
						script{
							try{
								sh'''
									//rm -rf /u02/Backup/App02NodeA.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
						
						sh'''
							//cd /u01
							//tar -cvf /u02/Backup/App02NodeA.tar.gz app
							echo "taking backup app02NodeA"
						'''
					}
				}
				
				stage('IDMNodeA Backup'){
					agent {
						label "$IDMNodeADev19"
					}
					steps{
						
						script{
							try{
								sh'''
									//rm -rf /u02/Backup/IDMNodeA.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
						
						sh '''
							//cd /u01
							//tar -cvf /u02/Backup/IDMNodeA.tar.gz app
							echo "taking backup IDMNodeA"
						'''
					}
				}
				
				stage('App01NodeB Backup'){
					agent {
						label "$App01NodeBDev19"
					}
					steps{
						when (expression { ${HA}==true}){
							script{	
								try{
									sh'''
										//rm -rf /u02/Backup/App01NodeB.tar.gz
									'''
									}catch(Exception e){
										throw e
									}
							}
							sh'''
								//cd /u01
								//tar -cvf /u02/Backup/App01NodeB.tar.gz app
								echo "taking backup app01NodeB"
							'''
						}
					}
				}
						
						
				stage('App02NodeB Backup'){
					agent {
						label "$App02NodeBDev19"
					}
					steps{
						when (expression { ${HA}==true}){
							script{
								try{
									sh'''
										//rm -rf /u02/Backup/App02NodeB.tar.gz
									'''
									}catch(Exception e){
										throw e
									}
							}	
							sh'''
								//cd /u01
								//tar -cvf /u02/Backup/App02NodeB.tar.gz app
								echo "taking backup app02NodeB"
							'''
						}
					}
				}
				stage('IDMNodeB Backup'){
					agent {
						label "$IDMNodeBDev19"
					}
					steps{
						when (expression { ${HA}==true}){
							script{
								try{
									sh'''
										//rm -rf /u02/Backup/IDMNodeB.tar.gz
									'''
									}catch(Exception e){
										throw e
									}
							}	
							sh'''
								//cd /u01
								//tar -cvf /u02/Backup/IDMNodeB.tar.gz app
								echo "taking backup idmNodeB"
							'''
						}
					}
				}
			}
		}
		stage('Starting DB'){
			agent {
				label "${DBDev19}"
			}
			steps{
				sh'''
					//cd /u01/
					//rm -rf startDB.py   || true
					//wget "http://kkm00bme.in.oracle.com:8080/job/Cloud_Automation_BATS/ws/startDB.py"
					//sudo -H -u gbuora python startDB.py ${DBCONTAINER} ${DBPLUGGABLE} /u01/app/oracle/
					echo "Starting db"
				'''
			}
		}
		
		stage('Tagging the nodes with start_server tag'){
			agent{
				node{
					label "$CHEF_WORKSTATION"
				}
			}
			steps{
				script{
					try{
						sh '''
							echo "Coldplay@123" | sudo -S /u01/workstation/chef-repo/knife_tag_delete_role.sh /u01/workstation/chef-repo/${HOST_LIST} stop_servers
							echo "Coldplay@123" | sudo -S /u01/workstation/chef-repo/knife_tag_assign_role.sh /u01/workstation/chef-repo/${HOST_LIST} start_servers "recipe[pgbu_reboot_new::start_servers_V7]" 
						'''
					}
					catch(Exception e){
						sh '''
							echo 'Unable to tag start_servers'
						'''
					}
				}
			}
		}
		
		stage('Starting servers in App01, App02 , IDM'){
			parallel {
				stage('App01NodeA'){
					agent {
						label "${App01NodeADev19}"
					}
					
					steps {
						sh '''
							//cd /tmp
							//chef-client -l debug -L startServer.log
							echo "running start server chef-client App01NodeA"
						'''
						
					}
				}
				
				stage('App02NodeA'){
					agent {
						label "${App02NodeADev19}"
					}
					
					steps {
						sh '''
							//cd /tmp
							//chef-client -l debug -L startServer.log
							echo "running start server chef-client App02NodeA"
						'''
						
					}
				}
				
				stage('IDMNodeA'){
					agent {
						label "${IDMNodeADev19}"
					}
					
					steps {
						sh '''
							//cd /tmp
							//chef-client -l debug -L startServer.log
							echo "running start server chef-client idmNodeA"
						'''
						
					}
				}
				
				stage('App01NodeB'){
					agent {
						label "${App01NodeBDev19}"
					}
					
					steps {
						when (expression { ${HA}==true}){
							sh '''
								//cd /tmp
								//chef-client -l debug -L stopServer.log
								echo "running start server chef-client App01NodeB"
							'''
						}
					}
				}
				
				stage('App02NodeB'){
					agent {
						label "${App02NodeBDev19}"
					}
					steps {
						when (expression { ${HA}==true}){
							sh '''
								//cd /tmp
								//chef-client -l debug -L stopServer.log
								echo "running start server chef-client App02NodeB"
							'''
						}				
					}
				}
				
				stage('IDMNodeB'){
					agent {
						label "${IDMNodeBDev19}"
					}
					
					steps {
						when (expression { ${HA}==true}){
							sh '''
								//cd /tmp
								//chef-client -l debug -L stopServer.log
								echo "running start server chef-client IDMNodeB"
							'''
						}
					}
				}
			}
		}
	}
}

