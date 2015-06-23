<?php


class search_manager {
	var 	$search_str;
	var		$search_path;
	var		$results;

	
	function __construct($str, $path)
	{
		$this->search_str = $str;
		printf("str = %s\n", $str);
		$this->search_path = $path;
		printf("path = %s\n", $path);
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
		$data = fread($file_handle, filesize($file));
		fclose($file_handle);
		$regx = "/" . $this->search_str . "/";
		if (preg_match('/' . $this->search_str . '/', $data, $matchs)) {
			printf("xxxxxx\n");
			printf($matchs[0]);
		}
	}
}

$search_mgr = new search_manager($_POST["search_str"], "/mnt/nfs/path_base");
$search_mgr->do_search();


?>