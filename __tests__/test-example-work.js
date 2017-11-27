import React from 'react';
import { shallow } from 'enzyme';
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import App from '../js/homepage';
configure ({ adapter: new Adapter()});




describe("EZ Test", () => {
  let component = shallow(<ExampleWork work={myWork}/>);

    it("Should be a 'section' element", () => {
      expect(component.type()).toEqual('section');
  });

  it("Should contain as many children as there are work examples", () => {
    expect(component.find("ExampleWorkBubble").length).toEqual(myWork.length);
  });

});
