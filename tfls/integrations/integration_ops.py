import math
import threading

from framework.tfls.base_tfl import BaseTfl
from framework.infra.infra import Infra

import timeout_decorator


class IntegrationsOps(BaseTfl):
    def __init__(self, infra: Infra=None, logger=None, tfls=None):
        super().__init__(infra=infra, logger=logger, tfls=tfls)

    @BaseTfl.step_wrapper(title="step_list_all_integrations", error="Failed to list all integrations")
    def step_list_all_integrations(self, tenant, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"listing all integrations for tenant {tenant.tid}")
        response = self.infra.rest.integrations.list_integrations(tenant=tenant)
        if positive:
            if response.status_code != 200:
                raise ValueError(
                    f"Failed to list all integrations: status_code: {response.status_code} content: {response.content}")
        else:
            if response.status_code == 200:
                raise ValueError(
                    f"Unexpectedly succeeded to list all integrations: status_code: {response.status_code} "
                    f"content: {response.content}")
        return response

    @BaseTfl.step_wrapper(title="step_create_integration", error="Failed to create integration")
    def step_create_integration(self, tenant, name, type, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"creating integration {name} of type {type} for tenant {tenant.tid}")
        response = self.infra.rest.integrations.create_integration(tenant=tenant, name=name, type=type)
        if positive:
            if response.status_code != 201:
                raise ValueError(
                    f"Failed to create integration: status_code: {response.status_code} content: {response.content}")
        else:
            if response.status_code == 201:
                raise ValueError(
                    f"Unexpectedly succeeded to create integration: status_code: {response.status_code} "
                    f"content: {response.content}")
        return response

    @BaseTfl.step_wrapper(title="step_create_integration", error="Failed to create integration")
    def step_create_integrations(self, tenant, integrations, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"creating integrations for tenant {tenant.tid}")
        for integration in integrations:
            self.logger.debug(f"creating integration {integration['name']} of type {integration['type']} on "
                              f"tenant {tenant.tid}")
            response = self.infra.rest.integrations.create_integration(tenant=tenant, name=integration['name'],
                                                                       type=integration['type'])
            if positive:
                if response.status_code != 201:
                    raise ValueError(
                        f"Failed to create integration: status_code: {response.status_code} content: {response.content}")
            else:
                if response.status_code == 201:
                    raise ValueError(
                        f"Unexpectedly succeeded to create integration: status_code: {response.status_code} "
                        f"content: {response.content}")


    @BaseTfl.step_wrapper(title="step_validate_integration_found", error="Failed to validate integration found")
    def step_validate_integration_found(self, tenant, name, type, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"validating integration {name} of type {type} for tenant {tenant.tid} is found and valid")
        response = self.infra.rest.integrations.list_integrations(tenant=tenant)
        integrations_found = [integration for integration in response.json()] if response.json() else []
        count = 0
        for integration in integrations_found:
            if integration['name'] == name and integration['type'] == type:
                count += 1

        if positive:
            if count != 1:
                raise ValueError(f"Found {count} integrations which matches the requested one: "
                                 f"status_code: {response.status_code} content: {response.content}")
        else:
            if count == 1:
                raise ValueError(f"Unexpectedly found {count} integrations matching the expected one: "
                                 f"status_code: {response.status_code} content: {response.content}")


    @BaseTfl.step_wrapper(title="step_delete_all_integrations", error="Failed to delete all integrations")
    def step_delete_all_integrations(self, tenant, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"deleting all integrations for tenant {tenant.tid}")
        response = self.infra.rest.integrations.list_integrations(tenant=tenant)
        if response.json():
            integrations_found = [integration for integration in response.json()]
            if integrations_found:
                for integration in integrations_found:
                    self.infra.rest.integrations.delete_integration(tenant=tenant, integration_id=integration['id'])


    @BaseTfl.step_wrapper(title="step_delete_integration", error="Failed to delete integration")
    def step_delete_integration(self, tenant, name, type, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"deleting integrations {name} of type {type} from tenant {tenant.tid}")
        response = self.infra.rest.integrations.list_integrations(tenant=tenant)
        integrations_found = [integration for integration in response.json()]
        for integration in integrations_found:
            if integration['name'] == name and integration['type'] == type:
                response = self.infra.rest.integrations.delete_integration(tenant=tenant,
                                                                           integration_id=integration['id'])
                if positive and response.status_code != 200:
                    raise ValueError(f"Failed to delete integration {name} of type {type} from tenant {tenant.tid}:"
                                     f"status_code: {response.status_code} content: {response.content}")
                if not positive and response.status_code == 200:
                    raise ValueError(f"Unexpectedly succeeded to delete integration {name} of type {type} from tenant "
                                     f"{tenant.tid}: status_code: {response.status_code} content: {response.content}")


    @BaseTfl.step_wrapper(title="step_update_integration", error="Failed to update integration")
    def step_update_integration(self, tenant, name, type, new_name, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"updating integrations {name} of type {type} within tenant {tenant.tid} "
                         f"with new name {new_name}")
        integration = self.infra.rest.integrations.get_integration_by_name_and_type(tenant=tenant, name=name, type=type)
        if integration:

            resp = self.infra.rest.integrations.update_integration(tenant=tenant, integration_id=integration['id'],
                                                                   name=new_name)
            if positive and resp.status_code != 200:
                raise ValueError(f"Failed to update integration {name} of type {type} from tenant {tenant.tid}:"
                                 f"status_code: {resp.status_code} content: {resp.content}")
            if not positive and resp.status_code == 200:
                raise ValueError(f"Unexpectedly succeeded to update integration {name} of type {type} from tenant "
                                 f"{tenant.tid}: status_code: {resp.status_code} content: {resp.content}")

        else:
            raise ValueError(f"Failed to update integration {name} of type {type} from tenant {tenant.tid}:"
                                     f"integration not found")


    @BaseTfl.step_wrapper(title="step_delete_integration", error="Failed to delete integration")
    def step_get_integration_by_id(self, tenant, integration_id, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"getting integrations with id {integration_id} from tenant {tenant.tid}")
        integration = self.infra.rest.integrations.get_integration_by_id(tenant=tenant, integration_id=integration_id)
        if integration:

            if positive and not integration:
                raise ValueError(f"Failed to get integration with id {integration_id} from tenant {tenant.tid}")
            if not positive and integration:
                raise ValueError(f"Unexpectedly succeeded to get integration with id {integration_id} from tenant "
                                 f"{tenant.tid}")
        return integration


    @BaseTfl.step_wrapper(title="step_validate_integrations_found", error="Failed to validate integrations found")
    def step_validate_integrations_found(self, tenant, integrations, positive=True, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"validating all integrations exist on tenant {tenant.tid}")
        response = self.infra.rest.integrations.list_integrations(tenant=tenant)
        integrations_found = [integration for integration in response.json()] if response.json() else []

        for integration in integrations:
            found = False
            for found_integration in integrations_found:
                if (found_integration['name'] == integration['name'] and found_integration['type'] ==
                        integration['type']):
                    found = True
                    break
            if not found and positive:
                raise ValueError(f"Integration {integration['name']} of type {integration['type']} was not found on "
                                 f"tenant {tenant.tid}. Exiting")
            if found and not positive:
                raise ValueError(f"Integration {integration['name']} of type {integration['type']} was unexpectedly "
                                 f"found on tenant {tenant.tid}. Exiting")


    @timeout_decorator.timeout(seconds=60)
    @BaseTfl.step_wrapper(title="step_list_all_integrations", error="Failed to list all integrations")
    def step_stress_list_all_integrations(self, tenant, positive=True, num_of_calls_per_minute=1000, **kwargs):
        """

        :param tenant:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"listing all integrations for tenant {tenant.tid}. executing {num_of_calls_per_minute} "
                         f"calls in parallel with 1 minute timeout")
        try:
            chunks = math.floor(num_of_calls_per_minute/60)
            leftover = num_of_calls_per_minute%60

            for chunk in range(0, 1000, chunks):
                threads = []
                for num in range(0, chunks):
                    t = threading.Thread(target=self.step_list_all_integrations, args=(tenant,))
                    threads.append(t)
                    t.start()
                for thd in threads:
                    thd.join(timeout=chunks*2)

            threads = []
            for num in range(leftover):
                t = threading.Thread(target=self.step_list_all_integrations, args=(tenant,))
                threads.append(t)
                t.start()
            for thd in threads:
                thd.join(timeout=chunks * 2)
        except Exception as err:
            raise ValueError(f"Was not able to complete {num_of_calls_per_minute} calls within one minute: {err}")

