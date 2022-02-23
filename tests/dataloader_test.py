# TODO: this is such an ugly patch
import sys 
sys.path.append("../")

import unittest 
import torch 
import dataloader
import torch.testing as testing

class DataloaderTest(unittest.TestCase): 

    def setUp(self):
        im_path = './test_data/grad_lounge.png'
        self.pds = dataloader.PhotoDataset(im_path)
        self.pdl = dataloader.getPhotoDataloader(im_path, batch_size=32, num_workers=1, shuffle=True)

        base_dir = './test_data/'
        self.sds = dataloader.SyntheticDataset(base_dir, 'train', 1, 50, 50)
        self.sdl = dataloader.getSyntheticDataloader(base_dir, 'train', 1, 50, 50, num_workers=1, shuffle=True)


    def test_photo_get_0th_idx(self):
        coords, rgb = self.pds[0]
        gt = torch.zeros((2,))
        testing.assert_close(coords, gt)
        self.assertEqual(rgb.shape, (3,))

    def test_photo_get_final_idx(self):
        coords, rgb = self.pds[403*538 - 1]
        gt = torch.FloatTensor([1.0, 1.0])
        testing.assert_close(coords, gt)
        self.assertEqual(rgb.shape, (3,))

    def test_photo_get_dataloader(self):
        dl_iter = iter(self.pdl)
        batch = next(dl_iter)
        coords, rgb = batch
        self.assertEqual(coords.shape, (32, 2))
        self.assertEqual(rgb.shape, (32, 3))

    def test_synthetic_focal_length(self): 
        # 0.5 * W / tan(0.5 * cam_angle_x) = 0.5 * 50 / tan(0.5 * 0.6) = 80.81820359
        self.assertAlmostEqual(self.sds.focal, 80.81820359)


    # I was going to test my rays but ummm, its kind of hard
    # def test_synthetic_get_ray(self):
    #     torch.manual_seed(0)
    #     idx = torch.Tensor([[44], [39]])
    #     batch = self.sds[0]
    #     origin, direc, rgba = batch['origin'], batch['direc'], batch['rgba']
    #     print(origin)
    #     gt_origin = torch.Tensor([[0.76, 0.56, 3.0]])
    #     testing.assert_close(origin, gt_origin)


if __name__ == '__main__':
    unittest.main(verbosity=2)
