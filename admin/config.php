<?php
require_once('sqlin.php');
$conf['debug']['level']=5;

/**/
$conf['db']['dsn']='mysql:host=localhost;dbname=xy_yule';
$conf['db']['user']='root';
$conf['db']['password']='';
$conf['db']['charset']='utf8';
$conf['db']['prename']='xy_';

$conf['safepass']='66668888';     //

$conf['cache']['expire']=0;
$conf['cache']['dir']='c\_cache/';     //
$conf['url_modal']=2;
$conf['action']['template']='wjinc/admin/';
$conf['action']['modals']='wjaction/admin/';
$conf['member']['sessionTime']=15*60;	//
$conf['node']['access']='http://localhost:65531';	//你好

error_reporting(E_ERROR & ~E_NOTICE);
ini_set('date.timezone', 'asia/shanghai');
ini_set('display_errors', 'Off');