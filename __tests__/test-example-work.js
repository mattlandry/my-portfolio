import React from 'react';
import { shallow } from 'enzyme';
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import ExampleWork from '../js/example-work';
configure ({ adapter: new Adapter()});

const myWork = [
  {
    'title': "Work Example 1",
    'image': {
      'desc': "example screenshot of a project involving code",
      'src': "images/example1.png",
      'comment': ""
    }
  },
  {
    'title': "Work Example 3",
    'image': {
      'desc': "serverless portfolio",
      'src': "images/example3.png",
      'comment': `Bengal cat” by roberto shabs is licensed under CC BY 2.0
                  https://www.flickr.com/photos/37287295@N00/2540855181`
    }
  }
];



describe("ExampleWork component", () => {
  let component = shallow(<ExampleWork work={myWork}/>);

    it("Should be a 'section' element", () => {
      console.log(component.debug());
  });
});
