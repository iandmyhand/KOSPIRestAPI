package com.blackvelvet.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.blackvelvet.cybos.bridge.cputil.ClassFactory;
import com.blackvelvet.cybos.bridge.cputil.ICpCybos;

@RestController
public class CPUtilController {

	private ICpCybos cpCybos;

    @RequestMapping("/util/cybos/isConnect")
    public int cybosIsConnect() {
    	if(cpCybos == null) {
    		cpCybos = ClassFactory.createCpCybos();
    	}
        return cpCybos.isConnect();
    }

}
