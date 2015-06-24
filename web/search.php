<?php


class search_manager {
	var 	$search_str;
	var		$search_path;
	var		$results;
	var		$link_list;

	
	function __construct($str, $path)
	{
		$this->search_str = $str;
		$this->search_path = $path;
	}
	
	function do_search()
	{
		if (!is_dir($this->search_path)) {
			return False;
		}
		
		if (strcmp(substr($this->search_path, -1), "/") == 0) {
			$this->search_path = substr($this->search_path, 1, strlen($this->search_path));
		}
		
		$this->search_all($this->search_path);
	}
	
	function search_all($path)
	{
		//printf("path = %s\n", $path);
		$handle = opendir($path);

		if ($handle) {
			while(false !== ($file = readdir($handle))) {
				if ($file != '.' && $file != '..') {
					$file_name = $path . "/" . $file;
					if (is_file($file_name)) {
						$this->search_one($file_name);
					} else {
						$this->search_all($file_name);
					}
				}
			}
		}
		
		closedir($handle);
	}
	
	function search_one($file)
	{
		//printf("search %s\n", $file);
		$file_handle = fopen($file, "r");
		//$data = fread($file_handle, filesize($file));
		$src_link = iconv('UTF-8', 'GB2312', fgets($file_handle));
		
		while (!feof($file_handle)) {
			$line = iconv('UTF-8', 'GB2312', fgets($file_handle));
			
			//if (preg_match('/' . $this->search_str . '/', $line, $matchs)) {
			if ($find_str = strstr($line, $this->search_str)) {
				$sub_str = substr($find_str, 0, 100);
				$this->results[$sub_str] = $file;
				$this->link_list[$sub_str] = $src_link;

				#echo "<a href=$file>$sub_str</a>";
				break;
			}
			
		}
		
		fclose($file_handle);
	}
	
	function print_all()
	{
		$i = 1;
		foreach($this->results as $key => $value) {
			$temp_page = iconv('UTF-8', 'GB2312', "网页快照");
			echo " $i $key...<a href = $value>$temp_page</a> </br>";
			$temp_link = $this->link_list[$key];
			echo "<a href =$temp_link>$temp_link</a></br></br>";
			$i++;
		}
	}
}

$search_mgr = new search_manager($_POST["search_str"], "/mnt/nfs/path_base");
$search_mgr->do_search();
$search_mgr->print_all();

?>