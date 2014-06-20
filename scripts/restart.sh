#! /bin/bash
export LANG=zh_CN.UTF-8

cd `dirname $0`
cd ..

mkdir -p log

source ~/.bashrc

PID_FILE='log/flask.pid'


if [ -f "$PID_FILE" ]
then
    old_pid=`cat $PID_FILE`
    for pid in `pgrep gunicorn`
    do  
        if [ "$pid" = "$old_pid" ]
        then
            kill -HUP $pid #通过主进程平滑重启
            echo "`date` --  HUP master worker: $pid" | tee -a log/restart.log
            exit 1
        fi  
    done
fi

#重新启动
pkill gunicorn
gunicorn -k gevent -w 2 -b "127.0.0.1:8888" -p "$PID_FILE" --access-logfile "log/access.log" run:app -D
echo "`date` --  Restart" | tee -a log/restart.log
