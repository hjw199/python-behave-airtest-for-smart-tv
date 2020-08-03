cd /home/hjw/OS_test
behave -f allure_behave.formatter:AllureFormatter -o "/home/hjw/OS_test/reports" ./features

crontab -e
30 23 * * * sh /home/hjw/OS_test/run.sh